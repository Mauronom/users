from dataclasses import dataclass
from datetime import datetime, timezone
from hex.mailing.domain.exceptions import MailNotFound, MailAlreadySent
from hex.mailing.domain.mail import MailStatus


@dataclass
class SendMail:
    c_name = "send.mail"
    mail_id: str


class SendMailHandler:
    def __init__(self, mail_repo, mail_sender, cid_image_repo=None, attachment_repo=None):
        self.mail_repo = mail_repo
        self.mail_sender = mail_sender
        self.cid_image_repo = cid_image_repo
        self.attachment_repo = attachment_repo

    def execute(self, cmd):
        mails = self.mail_repo.find_by_field("uuid", cmd.mail_id)
        if not mails:
            raise MailNotFound(cmd.mail_id)
        mail = mails[0]
        if mail.status == MailStatus.sent:
            raise MailAlreadySent
        mail_to_send = self._with_resolved_resources(mail)
        try:
            self.mail_sender.send(mail_to_send)
            mail.status = MailStatus.sent
            mail.send_date = datetime.now(timezone.utc)
        except Exception:
            mail.status = MailStatus.error
            self.mail_repo.save(mail)
            raise
        self.mail_repo.save(mail)

    def _with_resolved_resources(self, mail):
        needs_clone = (
            (self.cid_image_repo and mail.images) or
            (self.attachment_repo and mail.attachments)
        )
        if not needs_clone:
            return mail
        resolved = mail.clone()
        if self.cid_image_repo and mail.images:
            print(type(mail.images))
            print("From FsCidImageRepo: cids")
            
            for cid in mail.images.values():
                print(cid)
            resolved.images = {cid: self.cid_image_repo.find(path) for (cid,path) in mail.images.items()}
        if self.attachment_repo and mail.attachments:
            resolved.attachments = [self.attachment_repo.find(path) for path in mail.attachments]
        return resolved
