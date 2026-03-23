from hex.mailing.infra import MemoryContactsRepo, MemoryTemplatesRepo, MemoryMailsRepo, CommandBus
from hex.mailing.app import CreateMail, CreateMailHandler
from hex.mailing.domain import Contact, Template, Mail, MailStatus
from hex.mailing.domain import SubstitutionError


def make_contact(**kwargs):
    defaults = dict(uuid="c1", nom="Vida", mail="vida@test.com", web="", persona_contacte="", telefon="", notes="", data_enviat=None, idioma="ca")
    defaults.update(kwargs)
    return Contact(**defaults)


def make_template(**kwargs):
    defaults = dict(uuid="t1", subject="Hi {fest_name}", body="Hello {fest_name}", substitutions={"fest_name": "nom"}, attachments=[], images={})
    defaults.update(kwargs)
    return Template(**defaults)


def test_create_mail_success():
    contact = make_contact()
    template = make_template(substitutions={}, subject="Hi", body="Hello")
    c_repo = MemoryContactsRepo([contact])
    t_repo = MemoryTemplatesRepo([template])
    m_repo = MemoryMailsRepo([])
    h = CreateMailHandler(t_repo, c_repo, m_repo)
    c_bus = CommandBus()
    c_bus.subscribe(CreateMail, h)
    c_bus.dispatch(CreateMail(template_id="t1", contact_id="c1"))

    mails = m_repo.mails
    assert len(mails) == 1
    assert mails[0].to == "vida@test.com"


def test_create_mail_status_pending():
    contact = make_contact()
    template = make_template(substitutions={}, subject="Hi", body="Hello")
    c_repo = MemoryContactsRepo([contact])
    t_repo = MemoryTemplatesRepo([template])
    m_repo = MemoryMailsRepo([])
    h = CreateMailHandler(t_repo, c_repo, m_repo)
    c_bus = CommandBus()
    c_bus.subscribe(CreateMail, h)
    c_bus.dispatch(CreateMail(template_id="t1", contact_id="c1"))

    assert m_repo.mails[0].status == MailStatus.pending


def test_create_mail_substitution_applied():
    contact = make_contact(nom="Vida")
    template = make_template(subject="Hi {fest_name}", body="Hello {fest_name}", substitutions={"fest_name": "nom"})
    c_repo = MemoryContactsRepo([contact])
    t_repo = MemoryTemplatesRepo([template])
    m_repo = MemoryMailsRepo([])
    h = CreateMailHandler(t_repo, c_repo, m_repo)
    c_bus = CommandBus()
    c_bus.subscribe(CreateMail, h)
    c_bus.dispatch(CreateMail(template_id="t1", contact_id="c1"))

    mail = m_repo.mails[0]
    assert mail.body == "Hello Vida"
    assert mail.subject == "Hi Vida"


def test_create_mail_missing_field_raises():
    contact = make_contact()
    template = make_template(substitutions={"fest_name": "nonexistent_field"})
    c_repo = MemoryContactsRepo([contact])
    t_repo = MemoryTemplatesRepo([template])
    m_repo = MemoryMailsRepo([])
    h = CreateMailHandler(t_repo, c_repo, m_repo)
    c_bus = CommandBus()
    c_bus.subscribe(CreateMail, h)

    try:
        c_bus.dispatch(CreateMail(template_id="t1", contact_id="c1"))
    except SubstitutionError:
        pass
    else:
        assert False, "Expected SubstitutionError"
