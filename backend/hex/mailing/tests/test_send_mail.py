import pytest
from hex.mailing.infra import MemoryMailsRepo, CommandBus
from hex.mailing.app import SendMail, SendMailHandler
from hex.mailing.domain import Mail, MailStatus, Contact, MailNotFound, MailSenderPort, CidImageRepoPort, AttachmentRepoPort


def make_contact(**kwargs):
    defaults = dict(uuid="c1", nom="Vida", mail="vida@test.com", web="", persona_contacte="", telefon="", notes="", data_enviat=None, idioma="ca")
    defaults.update(kwargs)
    return Contact(**defaults)


def make_mail(**kwargs):
    defaults = dict(uuid="m1", status=MailStatus.pending, contact=make_contact(), subject="Hi", body="Hello")
    defaults.update(kwargs)
    return Mail(**defaults)


class FakeMailSender(MailSenderPort):
    def __init__(self, fail=False):
        self.sent = []
        self.fail = fail

    def send(self, mail):
        if self.fail:
            raise Exception("send failed")
        self.sent.append(mail)


class FakeCidImageRepo(CidImageRepoPort):
    def __init__(self, images):
        self.images = images

    def find(self, cid_name):
        return self.images.get(cid_name)


class FakeAttachmentRepo(AttachmentRepoPort):
    def __init__(self, attachments):
        self.attachments = attachments  # {path: (name, bytes)}

    def find(self, path):
        return self.attachments.get(path)


def test_send_mail_sets_status_to_sent():
    mail = make_mail()
    m_repo = MemoryMailsRepo([mail])
    sender = FakeMailSender()
    c_bus = CommandBus()
    c_bus.subscribe(SendMail, SendMailHandler(m_repo, sender))
    c_bus.dispatch(SendMail(mail_id="m1"))

    assert m_repo.mails[0].status == MailStatus.sent


def test_send_mail_updates_send_date():
    mail = make_mail()
    m_repo = MemoryMailsRepo([mail])
    sender = FakeMailSender()
    c_bus = CommandBus()
    c_bus.subscribe(SendMail, SendMailHandler(m_repo, sender))
    c_bus.dispatch(SendMail(mail_id="m1"))

    assert m_repo.mails[0].send_date is not None


def test_send_mail_not_found_raises():
    m_repo = MemoryMailsRepo([])
    sender = FakeMailSender()
    c_bus = CommandBus()
    c_bus.subscribe(SendMail, SendMailHandler(m_repo, sender))

    with pytest.raises(MailNotFound):
        c_bus.dispatch(SendMail(mail_id="nonexistent"))


def test_send_mail_sender_failure_sets_error_status():
    mail = make_mail()
    m_repo = MemoryMailsRepo([mail])
    sender = FakeMailSender(fail=True)
    c_bus = CommandBus()
    c_bus.subscribe(SendMail, SendMailHandler(m_repo, sender))

    with pytest.raises(Exception):
        c_bus.dispatch(SendMail(mail_id="m1"))

    assert m_repo.mails[0].status == MailStatus.error


def test_send_mail_passes_resolved_cid_images_to_sender():
    mail = make_mail(images={"sinoes": "mailing/img/sinoes.jpg"})
    m_repo = MemoryMailsRepo([mail])
    sender = FakeMailSender()
    image_repo = FakeCidImageRepo({"sinoes": b"img_bytes"})
    c_bus = CommandBus()
    c_bus.subscribe(SendMail, SendMailHandler(m_repo, sender, image_repo))
    c_bus.dispatch(SendMail(mail_id="m1"))

    assert sender.sent[0].images == {"sinoes": b"img_bytes"}


def test_send_mail_preserves_image_paths_in_repo():
    mail = make_mail(images={"sinoes": "mailing/img/sinoes.jpg"})
    m_repo = MemoryMailsRepo([mail])
    sender = FakeMailSender()
    image_repo = FakeCidImageRepo({"sinoes": b"img_bytes"})
    c_bus = CommandBus()
    c_bus.subscribe(SendMail, SendMailHandler(m_repo, sender, image_repo))
    c_bus.dispatch(SendMail(mail_id="m1"))

    assert m_repo.mails[0].images == {"sinoes": "mailing/img/sinoes.jpg"}


def test_send_mail_passes_resolved_attachments_to_sender():
    mail = make_mail(attachments=["mailing/attachments/foo.pdf"])
    m_repo = MemoryMailsRepo([mail])
    sender = FakeMailSender()
    attachment_repo = FakeAttachmentRepo({"mailing/attachments/foo.pdf": ("foo.pdf", b"pdf_bytes")})
    c_bus = CommandBus()
    c_bus.subscribe(SendMail, SendMailHandler(m_repo, sender, attachment_repo=attachment_repo))
    c_bus.dispatch(SendMail(mail_id="m1"))

    assert sender.sent[0].attachments == [("foo.pdf", b"pdf_bytes")]


def test_send_mail_preserves_attachment_paths_in_repo():
    mail = make_mail(attachments=["mailing/attachments/foo.pdf"])
    m_repo = MemoryMailsRepo([mail])
    sender = FakeMailSender()
    attachment_repo = FakeAttachmentRepo({"mailing/attachments/foo.pdf": ("foo.pdf", b"pdf_bytes")})
    c_bus = CommandBus()
    c_bus.subscribe(SendMail, SendMailHandler(m_repo, sender, attachment_repo=attachment_repo))
    c_bus.dispatch(SendMail(mail_id="m1"))

    assert m_repo.mails[0].attachments == ["mailing/attachments/foo.pdf"]
