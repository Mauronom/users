from dataclasses import dataclass
from datetime import datetime, timezone
from hex.mailing.domain.exceptions import MailNotFound, MailAlreadySent
from hex.mailing.domain.mail import MailStatus


@dataclass
class SendMail:
    c_name = "send.mail"
    mail_id: str


class SendMailHandler:
    def __init__(self, mail_repo, mail_sender):
        self.mail_repo = mail_repo
        self.mail_sender = mail_sender

    def execute(self, cmd):
        mails = self.mail_repo.find_by_field("uuid", cmd.mail_id)
        if not mails:
            raise MailNotFound(cmd.mail_id)
        mail = mails[0]
        if mail.status == MailStatus.sent:
            raise MailAlreadySent
        try:
            self.mail_sender.send(mail)
            mail.status = MailStatus.sent
            mail.send_date = datetime.now(timezone.utc)
        except Exception:
            mail.status = MailStatus.error
            self.mail_repo.save(mail)
            raise
        self.mail_repo.save(mail)
