from email.message import EmailMessage
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

    def account_confirmation(self, address, token):
        message = f"Ваше посилання для активації акаунту: {config.url}/activate/{token}"

        msg = EmailMessage()
        msg.set_content(message)

        msg["Subject"] = "Активація акаунту"
        msg["From"] = self.sender
        msg["To"] = address

        self.send(msg)
