import pandas as pd
import datetime
import pymssql
import socket
import os


# basic utility to print current timestamp and message
def pt(text, indent=False):
    if indent:
        print(f'                     {text}')
    else:
        print(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S') + f': {text}')


# coverts file name to full extension if being run on the VM (gb5-li-bpsn001)
def zfile(file, directory=__file__):
    '''
        Converts a relative file to an absolute file

        :param file: <str>
        :param directory: __file__
        :return: <str>

        Example:
        zfile('Query.sql', __file__) = S:/Operations/Data_Pipelines/Example/Query.sql
    '''
    if socket.gethostname() == 'gb5-li-bpsn001':
        file = os.path.join(os.path.dirname(directory), file)
    return file


# gets query from a .sql file
def get_query_from_file(file):
    '''
        :param file: <str> a .sql file which contains the query to run
        :return: <str>

        Example:
        get_query_from_file(thg.zfile('Queries/sales.sql'))
    '''
    pt(f'Retrieving Query from <{file}>')
    q = open(zfile(file), 'r', encoding='utf-8-sig')
    query = q.read()
    print_query = query.replace("\n", " ").strip()
    pt(f'Query Preview: <{print_query if len(print_query) < 50 else print_query[:50] + "..."}>')
    return query


# function to get data from sql
def sql_get_data(query=None, file=None, server='AAO-LI-AHCRP002.Thehutgroup.LOCAL', username=None, password=None):
    '''
    :param query: <str> query to run
    :param file: <str> a .sql file which contains the query to run
    :param server: <str> SQL server, defaults to 'AAO-LI-AHCRP002.Thehutgroup.LOCAL'
    :param username: <str> SQL username, defaults to windows authentication
    :param password: <str> SQL password, defaults to windows authentication
    :return: <pandas.dataframe>

    Example 1 (Using windows authentication):
    sql_get_data(query='SELECT TOP 10 * FROM Operations.dbo.Outbound (NOLOCK)')

    Example 2 (Using a service account & a file which stores the query):
    sql_get_data(file='query.sql',
                 server='AAO-LI-AHCRP002.Thehutgroup.LOCAL',
                 username='sa_bpswcopsql01',
                 password='examplepassword123'
                 )
    '''

    # print statements for query configurations & contents
    def print_query_statement(server, username, query, file=None):
        pt(f'Executing SQL Query')
        pt(f'SQL Server: {server}', indent=True)
        pt(f'SQL Username: {username if username is not None else "<Windows Authentication>"}', indent=True)
        if file != None:
            pt(f'Query File: {file}', indent=True)
        print_query = query.replace("\n", " ").strip()
        pt(f'Query Preview: <{print_query if len(print_query) < 50 else print_query[:50] + "..."}>', indent=True)

    # extract query from file (if applicable)
    if file != None:
        query = open(zfile(file), 'r', encoding='utf-8-sig').read()

    # get results
    print_query_statement(server, username, query, file)
    starting_timestamp = datetime.datetime.now()
    connection = pymssql.connect(server=server, user=username, password=password)
    df = pd.read_sql(sql=query, con=connection)
    ending_timestamp = datetime.datetime.now()
    runtime = ending_timestamp - starting_timestamp
    rows, columns = len(df), df.shape[1]
    pt(f'Dataframe Completed from SQL ({columns} columns x {rows} rows)')
    pt(f'Runtime: {runtime}', indent=True)
    return df


# function to execute sproc in sql
def sql_exec_sproc(sproc, server='AAO-LI-AHCRP002.Thehutgroup.LOCAL', username=None, password=None):
    '''
    :param sproc: <str> sproc to execute
    :param server: <str> SQL server, defaults to 'AAO-LI-AHCRP002.Thehutgroup.LOCAL'
    :param username: <str> SQL username, defaults to windows authentication
    :param password: <str> SQL password, defaults to windows authentication

    Example:
    sql_exec_sproc(sproc='Operations.dbo.usp_shipments',
                   server='AAO-LI-AHCRP002.Thehutgroup.LOCAL',
                   username='sa_bpswcopsql01',
                   password='examplepassword123'
                   )
    '''
    # print statements for query configurations & contents
    def print_query_statement(server, username, sproc):
        pt(f'Executing SQL Stored Procedure')
        pt(f'SQL Server: {server}', indent=True)
        pt(f'SQL Username: {username if username is not None else "<Windows Authentication>"}', indent=True)
        pt(f'Stored Procedure: <{sproc}>', indent=True)

    # run sproc
    print_query_statement(server, username, sproc)
    starting_timestamp = datetime.datetime.now()
    connection = pymssql.connect(server=server, user=username, password=password)
    cursor = connection.cursor()
    cursor.execute(f'EXEC {sproc}')
    connection.commit()
    connection.close()
    ending_timestamp = datetime.datetime.now()
    runtime = ending_timestamp - starting_timestamp
    pt(f'Stored Procedure executed successfully')
    pt(f'Runtime: {runtime}', indent=True)


# function to execute sproc in sql
def sql_exec_statement(statement=None, file=None, server='AAO-LI-AHCRP002.Thehutgroup.LOCAL', username=None, password=None):
    '''
    :param statement: <str> statement to execute
    :param file: <str> a .sql file which contains the query to run
    :param server: <str> SQL server, defaults to 'AAO-LI-AHCRP002.Thehutgroup.LOCAL'
    :param username: <str> SQL username, defaults to windows authentication
    :param password: <str> SQL password, defaults to windows authentication

    Example 1 (Using windows authentication):
    sql_exec_statement(statement='DELETE FROM Operations.dbo.usp_shipments WHERE full_date = "2010-01-01"')

    Example 2 (Using a service account & a file which stores the statement):
    sql_exec_statement(file='query.sql',
                       server='AAO-LI-AHCRP002.Thehutgroup.LOCAL',
                       username='sa_bpswcopsql01',
                       password='examplepassword123'
    '''

    # extract statement from file (if applicable)
    if file != None:
        statement = open(zfile(file), 'r', encoding='utf-8-sig').read()

    # print statements for query configurations & contents
    def print_query_statement(server, username, statement, file=None):
        pt(f'Executing SQL Statement')
        pt(f'SQL Server: {server}', indent=True)
        pt(f'SQL Username: {username if username is not None else "<Windows Authentication>"}', indent=True)
        if file != None:
            pt(f'File: {file}', indent=True)
        print_statement = statement.replace("\n", " ").strip()
        pt(f'Statement: <{print_statement if len(print_statement) < 50  else print_statement[:50]+"..."}>', indent=True)

    # run statement
    print_query_statement(server, username, statement, file)
    starting_timestamp = datetime.datetime.now()
    connection = pymssql.connect(server=server, user=username, password=password)
    cursor = connection.cursor()
    cursor.execute(statement)
    connection.commit()
    connection.close()
    ending_timestamp = datetime.datetime.now()
    runtime = ending_timestamp - starting_timestamp
    pt(f'Statement executed successfully')
    pt(f'Runtime: {runtime}', indent=True)


# function to upload a pandas dataframe to SQL server
def sql_insert_df(df, column_types, table, server='AAO-LI-AHCRP002.Thehutgroup.LOCAL', username=None, password=None,
                  chunksize=999, print_insert_statement=False, print_rows_inserted=False):
    """
    :param df: <pandas.dataframe> dataframe to upload
    :param column_types: <dict> dictionary of column names and data type
    :param table: <str> destination table name
    :param server: <str> SQL server, defaults to 'AAO-LI-AHCRP002.Thehutgroup.LOCAL'
    :param username: <str> SQL username, defaults to windows authentication
    :param password: <str> SQL password, defaults to windows authentication
    :param chunksize: <int> number of rows to insert at once, defaults to 999
    :param print_insert_statement: <bool> prints each insert statement, useful for troubleshooting, defaults to False
    :param print_rows_inserted: <bool> prints no. of rows inserted per chunk, useful for troubleshooting, defaults to False

    Example:
    sql_insert_df(df=pd.DataFrame({'site': 'Myprotein',
                                   'units': 64321,
                                   'order_date': datetime.date(2023,1,1),
                                   'revenue': 104662.59,
                                   'last_updated': datetime.datetime.now()
                                   }),
                  column_types={'site': 'varchar',
                                'units': 'int',
                                'order_date': 'date',
                                'revenue': 'float',
                                'last_updated": 'datetime'
                                },
                  table='Operations.dbo.Shipments',
                  server='AAO-LI-AHCRP002.Thehutgroup.LOCAL',
                  username='sa_bpswcopsql01',
                  password='examplepassword123',
                  chunksize=999,
                  print_insert_statement=False
                  )
    """

    # function to format value to upload
    def format_value(value, column_type):
        new_value = ''
        if str(value) in ['None', 'nan', 'NaT']:
            new_value = 'NULL'
        elif column_type.lower() == 'date':
            if isinstance(value, datetime.date):
                new_value = f"'{value.strftime('%Y-%m-%d')}'"
        elif column_type.lower() == 'datetime':
            if isinstance(value, datetime.datetime):
                new_value = f"'{value.strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]}'"
        elif column_type.lower() == 'int':
            new_value = f'{int(value)}'
        elif column_type.lower() == 'float':
            new_value = f'{float(value)}'
        else:
            new_value = f"'{value}'"
        return new_value

    # connect to SQL
    starting_timestamp = datetime.datetime.now()
    pt(f'Connecting to SQL to Upload Dataframe')
    pt(f'SQL Server: {server}', indent=True)
    pt(f'SQL Username: {username if username is not None else "<Windows Authentication>"}', indent=True)
    pt(f'Destination Table: {table}', indent=True)
    pt(f'Dataframe dimensions: ({df.shape[1]} columns x {len(df)} rows)', indent=True)
    pt(f'Chunksize: {chunksize}', indent=True)
    connection = pymssql.connect(server=server, user=username, password=password)
    cursor = connection.cursor()
    pt(f'SQL Connection Successful')

    # build insert statements
    insert_string = ''
    row_number = 1
    for index, row in df.iterrows():
        column_title, column_value = [], []
        for column in column_types:
            column_title.append(column)
            column_value.append(format_value(row[column], column_types[column]))
        insert_column_value, insert_column_title = ',', ','
        single_string = f'INSERT INTO {table} ({insert_column_title.join(column_title)}) VALUES ({insert_column_value.join(column_value)})'
        if print_insert_statement:
            pt(f'Row {row_number}: {single_string}')
        insert_string += single_string
        if row_number % chunksize == 0:
            cursor.execute(insert_string)
            connection.commit()
            insert_string = ''
            if print_rows_inserted:
                pt(f'Inserted up to row {row_number}')
        row_number += 1
    if insert_string != '':
        cursor.execute(insert_string)
        connection.commit()
        if print_rows_inserted:
            pt(f'Inserted up to row {len(df)}')

    # print complete
    pt('Dataframe upload complete')
    pt(f'Runtime: {datetime.datetime.now() - starting_timestamp}', indent=True)

