from pathlib import Path
from hex.mailing.domain import ContactsRepo, TemplatesRepo, MailsRepo, CidImageRepoPort, AttachmentRepoPort


class MemoryContactsRepo(ContactsRepo):
    def __init__(self, init_contacts):
        self.contacts = init_contacts

    def save(self, contact):
        self.contacts.append(contact.clone())

    def find_all(self):
        return [c.clone() for c in self.contacts]

    def find_by_field(self, field, value):
        return [c for c in self.contacts if getattr(c, field) == value]


class MemoryTemplatesRepo(TemplatesRepo):
    def __init__(self, init_templates):
        self.templates = init_templates

    def save(self, template):
        self.templates.append(template.clone())

    def find_all(self):
        return [t.clone() for t in self.templates]

    def find_by_field(self, field, value):
        return [t for t in self.templates if getattr(t, field) == value]


class MemoryMailsRepo(MailsRepo):
    def __init__(self, init_mails):
        self.mails = init_mails

    def save(self, mail):
        self.mails.append(mail.clone())

    def find_all(self):
        return [m.clone() for m in self.mails]

    def find_by_field(self, field, value):
        return [m for m in self.mails if getattr(m, field) == value]


class DjangoContactsRepo(ContactsRepo):
    def save(self, contact):
        from mailing.models import ContactModel
        ContactModel.objects.update_or_create(
            uuid=contact.uuid,
            defaults={"nom": contact.nom, "mail": contact.mail, "web": contact.web, "persona_contacte": contact.persona_contacte, "telefon": contact.telefon, "notes": contact.notes, "data_enviat": contact.data_enviat, "idioma": contact.idioma},
        )

    def find_all(self):
        from mailing.models import ContactModel
        return [self._to_domain(c) for c in ContactModel.objects.all()]

    def find_by_field(self, field, value):
        from mailing.models import ContactModel
        return [self._to_domain(c) for c in ContactModel.objects.filter(**{field: value})]

    def _to_domain(self, obj):
        from hex.mailing.domain import Contact
        return Contact(uuid=str(obj.uuid), nom=obj.nom, mail=obj.mail, web=obj.web, persona_contacte=obj.persona_contacte, telefon=obj.telefon, notes=obj.notes, data_enviat=obj.data_enviat, idioma=obj.idioma)


class DjangoTemplatesRepo(TemplatesRepo):
    def save(self, template):
        from mailing.models import TemplateModel
        TemplateModel.objects.update_or_create(
            uuid=template.uuid,
            defaults={"subject": template.subject, "body": template.body, "substitutions": template.substitutions, "attachments": template.attachments, "images": template.images},
        )

    def find_all(self):
        from mailing.models import TemplateModel
        return [self._to_domain(t) for t in TemplateModel.objects.all()]

    def find_by_field(self, field, value):
        from mailing.models import TemplateModel
        return [self._to_domain(t) for t in TemplateModel.objects.filter(**{field: value})]

    def _to_domain(self, obj):
        from hex.mailing.domain import Template
        return Template(uuid=str(obj.uuid), subject=obj.subject, body=obj.body, substitutions=obj.substitutions, attachments=obj.attachments, images=obj.images)


class DjangoMailsRepo(MailsRepo):
    def save(self, mail):
        from mailing.models import MailModel, ContactModel
        contact_obj = ContactModel.objects.get(uuid=mail.contact.uuid)
        MailModel.objects.update_or_create(
            uuid=mail.uuid,
            defaults={"send_date": mail.send_date, "status": mail.status.value, "contact": contact_obj, "subject": mail.subject, "body": mail.body, "attachments": mail.attachments, "images": mail.images},
        )

    def find_all(self):
        from mailing.models import MailModel
        return [self._to_domain(m) for m in MailModel.objects.select_related("contact").all()]

    def find_by_field(self, field, value):
        from mailing.models import MailModel
        return [self._to_domain(m) for m in MailModel.objects.select_related("contact").filter(**{field: value})]

    def _to_domain(self, obj):
        from hex.mailing.domain import Mail, MailStatus, Contact
        contact = Contact(uuid=str(obj.contact.uuid), nom=obj.contact.nom, mail=obj.contact.mail, web=obj.contact.web, persona_contacte=obj.contact.persona_contacte, telefon=obj.contact.telefon, notes=obj.contact.notes, data_enviat=obj.contact.data_enviat, idioma=obj.contact.idioma) if obj.contact else None
        return Mail(uuid=str(obj.uuid), send_date=obj.send_date, status=MailStatus(obj.status), contact=contact, subject=obj.subject, body=obj.body, attachments=obj.attachments, images=obj.images)


class FsCidImageRepo(CidImageRepoPort):
    def __init__(self, img_dir):
        self.img_dir = Path(img_dir)

    def find(self, cid_name: str) -> bytes:
        for f in self.img_dir.iterdir():
            if f.stem == cid_name:
                return f.read_bytes()
        return None


class FsAttachmentRepo(AttachmentRepoPort):
    def __init__(self, attachments_dir):
        self.attachments_dir = Path(attachments_dir)

    def find(self, path: str) -> tuple:
        f = Path(path)
        return (f.name, f.read_bytes())
