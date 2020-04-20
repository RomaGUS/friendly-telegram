from email.message import EmailMessage
from flask import render_template
import smtplib
import config

class Email(object):
    def __init__(self):
        self.host = config.smtp["host"]
        self.port = config.smtp["port"]
        self.sender = config.smtp["username"]
        self.password = config.smtp["password"]

    def send(self, msg):
        with smtplib.SMTP(self.host, self.port) as server:
            server.login(self.sender, self.password)
            server.send_message(msg)
            server.quit()

    def account_confirmation(self, account, token):
        message = render_template(
            "emails/activate.html",
            username=account.username,
            url=config.url,
            token=token
        )

        msg = EmailMessage()
        msg.set_content(message, subtype="html")

        msg["Subject"] = "Активація акаунту"
        msg["From"] = self.sender
        msg["To"] = account.email

        self.send(msg)

    def password_reset(self, account, token):
        message = render_template(
            "emails/reset.html",
            username=account.username,
            url=config.url,
            token=token
        )

        msg = EmailMessage()
        msg.set_content(message, subtype="html")

        msg["Subject"] = "Скидання паролю"
        msg["From"] = self.sender
        msg["To"] = account.email

        self.send(msg)
