import os
import smtplib
import email
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from datetime import datetime
from config import config

smtp_server = None  # Global variable to hold the SMTP connection

def connect_to_smtp():
    global smtp_server
    if smtp_server is None or not smtp_server.noop()[0] == 250:  # Check if connected or connection lost
        smtp_server = smtplib.SMTP(config.SMTP_SERVER, config.SMTP_PORT)
        smtp_server.starttls()
        smtp_server.login(config.SMTP_USERNAME, config.SMTP_PASSWORD)

def send_email(to, subject, body, cc=None, bcc=None, attachments=None, html=False):
    msg = MIMEMultipart()
    msg['From'] = config.EMAIL_FROM_ADDRESS
    msg['To'] = ", ".join(to)
    if cc:
        msg['Cc'] = ", ".join(cc)
    if bcc:
        msg['Bcc'] = ", ".join(bcc)
    msg['Subject'] = subject

    if html:
        msg.attach(MIMEText(body, 'html'))
    else:
        msg.attach(MIMEText(body, 'plain'))

    if attachments:
        for attachment in attachments:
            with open(attachment, 'rb') as f:
                part = MIMEApplication(f.read(), Name=os.path.basename(attachment))
                part['Content-Disposition'] = f'attachment; filename="{os.path.basename(attachment)}"'
                msg.attach(part)

    try:
        connect_to_smtp()  # Ensure SMTP connection is established
        recipients = to + (cc if cc else []) + (bcc if bcc else [])
        smtp_server.sendmail(config.EMAIL_FROM_ADDRESS, recipients, msg.as_string())
    except smtplib.SMTPException as e:
        save_failed_email(msg)
        raise e

def save_failed_email(msg):
    if not os.path.exists(config.EMAIL_QUEUE_DIRECTORY):
        os.makedirs(config.EMAIL_QUEUE_DIRECTORY)
    failed_email_path = os.path.join(config.EMAIL_QUEUE_DIRECTORY, f"failed_{int(datetime.now().timestamp())}.eml")
    with open(failed_email_path, 'w') as f:
        f.write(msg.as_string())

def check_and_resend_failed_emails():
    if not os.path.exists(config.EMAIL_QUEUE_DIRECTORY):
        return
    for filename in os.listdir(config.EMAIL_QUEUE_DIRECTORY):
        file_path = os.path.join(config.EMAIL_QUEUE_DIRECTORY, filename)
        with open(file_path, 'r') as f:
            msg = email.message_from_file(f)
        try:
            connect_to_smtp()  # Ensure SMTP connection is established
            recipients = msg['To'].split(", ") + msg.get_all('Cc', []) + msg.get_all('Bcc', [])
            smtp_server.sendmail(config.EMAIL_FROM_ADDRESS, recipients, msg.as_string())
            os.remove(file_path)
        except smtplib.SMTPException:
            continue
