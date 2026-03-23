from enum import Enum


class MailStatus(Enum):
    pending = "pending"
    sent = "sent"
    error = "error"


class Mail:
    def __init__(self, uuid="", send_date=None, status=MailStatus.pending, to="", subject="", body="", attachments=None, images=None):
        self.uuid = uuid
        self.send_date = send_date
        self.status = status
        self.to = to
        self.subject = subject
        self.body = body
        self.attachments = attachments if attachments is not None else []
        self.images = images if images is not None else {}

    def clone(self):
        return Mail(self.uuid, self.send_date, self.status, self.to, self.subject, self.body, list(self.attachments), dict(self.images))

    def __eq__(self, other):
        return self.uuid == other.uuid

    def to_primitive(self):
        return {"uuid": self.uuid, "send_date": self.send_date, "status": self.status.value, "to": self.to, "subject": self.subject, "body": self.body, "attachments": self.attachments, "images": self.images}
