import smtplib
import ssl
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import queue
import threading
from dotenv import load_dotenv
import os
import time

load_dotenv()

class MailService:
    '''Mail service with a queue for non-blocking email sending.'''
    def __init__(self, max_retries=3, retry_delay=5):
        self.smtp_server = os.getenv("SMTP_SERVER")
        self.port = int(os.getenv("SMTP_PORT"))
        self.password = os.getenv("SMTP_PASSWORD")
        self.sender_email = os.getenv("SENDER_EMAIL")
        self.context = ssl.create_default_context()
        self.max_retries = max_retries
        self.retry_delay = retry_delay

        self.email_queue = queue.Queue()
        self.start_workers()

    def start_workers(self):
        '''Start worker threads to process email sending tasks.'''
        for _ in range(2):  # Number of worker threads two
            threading.Thread(target=self.worker, daemon=True).start()

    def worker(self):
        '''Worker thread to process email sending tasks from the queue.'''
        while True:
            template, receiver_email, name, subject = self.email_queue.get()
            self._send_mail(template, receiver_email, name, subject)
            self.email_queue.task_done()

    def send_mail(self, template, receiver_email, name, subject):
        '''Enqueue email sending task.'''
        self.email_queue.put((template, receiver_email, name, subject))

    def _send_mail(self, template, receiver_email, name, subject):
        '''Internal method to send an email with retry mechanism.'''
        message = MIMEMultipart('alternative')
        message["Subject"] = subject
        message["From"] = self.sender_email
        message["To"] = receiver_email

        text = f"Hi, {name}\n{template}"
        html = f"""
        <html>
          <body>
            <h2>Hi, {name}</h2>
            <p>{template}</p>
          </body>
        </html>
        """

        part1 = MIMEText(text, "plain")
        part2 = MIMEText(html, "html")
        message.attach(part1)
        message.attach(part2)

        for attempt in range(self.max_retries):
            try:
                with smtplib.SMTP_SSL(self.smtp_server, self.port, context=self.context) as server:
                    server.login(self.sender_email, self.password)
                    server.sendmail(self.sender_email, receiver_email, message.as_string())
                break
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
                if attempt + 1 < self.max_retries:
                    time.sleep(self.retry_delay)  # Wait
                else:
                    print(f"Failed to send email to {receiver_email} after {self.max_retries} attempts.")
