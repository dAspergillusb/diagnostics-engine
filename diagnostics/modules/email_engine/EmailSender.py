from smtplib import SMTP
from email.mime.text import MIMEText
from diagnostics.modules.config import MAIL_LOGIN, MAIL_PASSWORD


class EmailSender(SMTP):

    def __init__(self, subject: str, recipient: str, message: str):
        host: str = "smtp.beget.com"
        port: int = 2525
        self.recipient = recipient
        self.full_message: MIMEText = MIMEText(message)
        self.full_message["Subject"] = subject
        self.full_message["From"] = MAIL_LOGIN
        self.full_message["To"] = recipient
        super().__init__(host=host, port=port)
        self.starttls()
        self.login(
            user=MAIL_LOGIN,
            password=MAIL_PASSWORD
        )

    def send_mail(self):
        self.sendmail(
            from_addr=MAIL_LOGIN,
            to_addrs=self.recipient,
            msg=self.full_message.as_string()
        )

    def close_connection(self):
        self.quit()


if __name__ == '__main__':
    message_ = "Для того, чтобы осстановить пароль, перейдите по ссылке снизу:\n"
    mail = EmailSender(
        MAIL_LOGIN,
        message_
    )
    mail.send_mail()
    mail.quit()
