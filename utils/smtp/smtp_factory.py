import os
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from dotenv import load_dotenv, find_dotenv


class EmailSender:
    def __init__(self):
        load_dotenv(find_dotenv())

        self.smtp_server = os.environ["SMTP_SERVER"]
        self.smtp_port = int(os.environ["SMTP_PORT"])
        self.sender_email = os.environ["SMTP_SENDER_EMAIL"]
        self.sender_password = os.environ["SMTP_SENDER_PASSWORD"]

        self.msg = MIMEMultipart()
        self.msg['From'] = self.sender_email
        self.msg['To'] = os.environ["SMTP_RECIPIENT_EMAIL"]
        self.msg['Subject'] = os.environ["SMTP_SUBJECT"]

    async def send_email(self, body):
        self.msg.attach(MIMEText(body, 'plain', 'utf-8'))

        try:
            with smtplib.SMTP(self.smtp_server, self.smtp_port) as server:
                server.starttls()
                server.login(self.sender_email, self.sender_password)
                server.send_message(self.msg)
        except Exception as e:
            print(f'Error while sending email: {e}')