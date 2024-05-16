#!/usr/bin/env python3
"""Mail service"""
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText


class MailService:
    '''mail service'''
    __SMTP_SERVER = "smtp.gmail.com"
    __PORT = 465  # For SSL
    __PASSWORD = 'ebks pxnu iopz qevj'
    # Create a secure SSL context
    __CONTEXT = ssl.create_default_context()
    __SENDER_EMAIL = "abdofola67@gmail.com"

    def send_mail(self, template, receiver_email, name):
        '''send receiver_email to user'''
        message = MIMEMultipart('alternative')
        message["Subject"] = ""
        message["From"] = self.__SENDER_EMAIL
        message["To"] = receiver_email

        # Create the plain-text and HTML version of your message
        TEXT = f"""\
        Hi, {name}
        {template}
        """
        HTML = f"""\
        <html>
          <body>
            <h2>Hi, {name}</h2>
            <p>
               {template}
            </p>
          </body>
        </html>
        """
        # Turn these into plain/html MIMEText objects
        part1 = MIMEText(TEXT, "plain")
        part2 = MIMEText(HTML, "html")

        # Add HTML/plain-text parts to MIMEMultipart message
        # The receiver_email client will try to render the last part first
        message.attach(part1)
        message.attach(part2)

        try:
            with smtplib.SMTP_SSL(self.__SMTP_SERVER, self.__PORT,
                                  context=self.__CONTEXT) as server:
                server.login(self.__SENDER_EMAIL, self.__PASSWORD)
                # Send receiver_email here
                server.sendmail(self.__SENDER_EMAIL,
                                receiver_email, message.as_string())
        except Exception as e:
            print(f"An error occurred while sending the email: {e}")
