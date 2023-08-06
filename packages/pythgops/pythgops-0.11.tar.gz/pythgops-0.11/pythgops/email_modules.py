import socket
import os
import win32com.client as win32
from email import encoders
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from smtplib import SMTP, SMTPException
from .utilities import pt


def email(to_list, cc_list, body, subject, attachments_list, send=False):
    """
    Basic Email Function

    Parameters:
       to_list (list): List of recipients for the email
       e.g. ['hello@thg.com', 'test@thehutgroup.com']

       cc_list (list): List of CC's for the email
       e.g. ['hello@thg.com', 'test@thehutgroup.com']

       body (str): Email body in HTML format
       e.g. This is the email body

       subject (str): Subject line
       e.g. Daily Report

       attachments_list (str): List of attachments
       e.g. ['export.xlsx', 'graph_1.jpg']

       send (bool): Sends email if True; Displays email if False
    """
    if socket.gethostname() == 'gb5-li-bpsn001':
        email = MIMEMultipart()
        sender = 'operations.reporting@thehutgroup.com'
        email['From'] = sender

        # email send list
        to = '; '
        receiver = to.join(to_list)
        email['To'] = receiver

        # email cc list
        cc = '; '
        receiver_cc = cc.join(cc_list)
        email['Cc'] = receiver_cc

        # subject & body
        email['Subject'] = subject
        email.attach(MIMEText(body, 'HTML'))

        # attachments // automatically assigns a content_id (CID) based on file name
        for file in attachments_list:
            with open(os.path.join(os.path.dirname(__file__), file), "rb") as attachment:
                part = MIMEBase('application', "octet-stream")
                part.set_payload(attachment.read())
                encoders.encode_base64(part)
                part.add_header('Content-Disposition', f'attachment; filename= {file}')
                part.add_header('X-Atachment-Id', f'{file}')
                if file[-4:] == '.jpg' or file[-4:] == '.png' or file[-5:] == '.jpeg':
                    part.add_header('Content-ID', f'{file}')
                email.attach(part)
                attachment.close()

        # Send Email
        if send:
            with SMTP(host="fortimail.gslb.thehut.local", port=25) as smtp:
                try:
                    smtp.sendmail(sender, receiver.split(';') + receiver_cc.split(';'), email.as_string())
                    pt('Email Sent!')
                except SMTPException as error:
                    pt(f'Email not sent ({error})')
        else:
            pt('Unable to display email as script is triggered on gb5-li-bpsn001')

    else:
        outlook = win32.Dispatch('outlook.application')
        email = outlook.CreateItem(0)

        # email send list
        to = '; '
        email.To = to.join(to_list)

        # email cc list
        cc = '; '
        email.CC = cc.join(cc_list)

        # subject & body
        email.Subject = subject
        email.HTMLBody = body

        # attachments // automatically assigns a content_id (CID) based on file name
        for file in attachments_list:
            if file[-4:] == '.jpg' or file[-4:] == '.png' or file[-5:] == '.jpeg':
                attachment = email.Attachments.Add(os.getcwd() + f'/{file}')
                attachment.PropertyAccessor.SetProperty("http://schemas.microsoft.com/mapi/proptag/0x3712001F",
                                                        f'{file}')
            else:
                email.Attachments.Add(os.getcwd() + f'/{file}')

        if send:
            email.Send()
            pt('Email Sent!')
        else:
            email.Display()
            pt('Email Displayed!')
