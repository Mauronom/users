class Template:
    def __init__(self, uuid="", subject="", body="", substitutions=None, attachments=None, images=None):
        self.uuid = uuid
        self.subject = subject
        self.body = body
        self.substitutions = substitutions if substitutions is not None else {}
        self.attachments = attachments if attachments is not None else []
        self.images = images if images is not None else {}

    def clone(self):
        return Template(self.uuid, self.subject, self.body, dict(self.substitutions), list(self.attachments), dict(self.images))

    def __eq__(self, other):
        return self.uuid == other.uuid

    def to_primitive(self):
        return {"uuid": self.uuid, "subject": self.subject, "body": self.body, "substitutions": self.substitutions, "attachments": self.attachments, "images": self.images}
