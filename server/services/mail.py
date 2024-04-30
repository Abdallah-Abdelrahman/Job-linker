#!/usr/bin/env python3
"""Mail service"""
import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

# import getpass


class EmailService:
    def __init__(self, smtp_server, port, sender_email, password):
        self.smtp_server = smtp_server
        self.port = port
        self.sender_email = sender_email
        self.password = password
        self.context = ssl.create_default_context()

    def send_email(self, receiver_email, subject, text, html):
        message = MIMEMultipart("alternative")
        message["Subject"] = subject
        message["From"] = self.sender_email
        message["To"] = receiver_email

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")

        message.attach(part1)
        message.attach(part2)

        with smtplib.SMTP_SSL(
            self.smtp_server, self.port, context=self.context
        ) as server:
            server.login(self.sender_email, self.password)
            server.sendmail(
                    self.sender_email,
                    receiver_email,
                    message.as_string()
                    )


# SMTP_SERVER = "smtp.gmail.com"
# PORT = 465  # For SSL
# PASSWORD = 'ebks pxnu iopz qevj'
# Create a secure SSL context
# CONTEXT = ssl.create_default_context()
# SENDER_EMAIL = "abdofola67@gmail.com"
# RECEIVER_EMAIL = "mo7amedelfadil@gmail.com"
# MESSAGE = MIMEMultipart('alternative')
# MESSAGE["Subject"] = "RESP"
# MESSAGE["From"] = SENDER_EMAIL
# MESSAGE["To"] = RECEIVER_EMAIL

# Create the plain-text and HTML version of your message
# TEXT = """\
# Hi,
# How are you?
# Real Python has many great tutorials:
# www.realpython.com"""
# HTML = """\
# <html>
#  <body>
#    <h2>Hi,</h2>
#    <p>
#       How are you?<br>
#       <a href="http://www.realpython.com">Real Python</a>
#       has many great tutorials, don't forget to check it out :)<br>
#       <code>BTW how are you doing so far in your project ???</code>
#    </p>
#  </body>
# </html>
# """

# Turn these into plain/html MIMEText objects
# part1 = MIMEText(TEXT, "plain")
# part2 = MIMEText(HTML, "html")

# Add HTML/plain-text parts to MIMEMultipart message
# The email client will try to render the last part first
# MESSAGE.attach(part1)
# MESSAGE.attach(part2)

# with smtplib.SMTP_SSL(SMTP_SERVER, PORT, context=CONTEXT) as server:
#    server.login(SENDER_EMAIL, PASSWORD)
# Send email here
#    server.sendmail(SENDER_EMAIL, RECEIVER_EMAIL, MESSAGE.as_string())
