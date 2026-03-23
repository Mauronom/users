import uuid as uuid_lib
from dataclasses import dataclass
from hex.mailing.domain import Mail, MailStatus
from hex.mailing.domain import ContactNotFound, TemplateNotFound, SubstitutionError


@dataclass
class CreateMail:
    c_name = "create.mail"
    template_id: str
    contact_id: str


class CreateMailHandler:
    def __init__(self, template_repo, contact_repo, mail_repo):
        self.template_repo = template_repo
        self.contact_repo = contact_repo
        self.mail_repo = mail_repo

    def execute(self, cmd):
        templates = self.template_repo.find_by_field("uuid", cmd.template_id)
        if not templates:
            raise TemplateNotFound()
        template = templates[0]

        contacts = self.contact_repo.find_by_field("uuid", cmd.contact_id)
        if not contacts:
            raise ContactNotFound()
        contact = contacts[0]

        subject = template.subject
        body = template.body
        for placeholder, contact_field in template.substitutions.items():
            value = getattr(contact, contact_field, None)
            if value is None:
                raise SubstitutionError(f"Contact has no field '{contact_field}'")
            subject = subject.replace("{" + placeholder + "}", str(value))
            body = body.replace("{" + placeholder + "}", str(value))

        mail = Mail(
            uuid=str(uuid_lib.uuid4()),
            send_date=None,
            status=MailStatus.pending,
            to=contact.mail,
            subject=subject,
            body=body,
            attachments=list(template.attachments),
            images=dict(template.images),
        )
        self.mail_repo.save(mail)
        return "ok"
