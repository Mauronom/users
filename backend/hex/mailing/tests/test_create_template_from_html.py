from hex.mailing.infra import MemoryTemplatesRepo
from hex.mailing.app import CreateTemplateFromHtml, CreateTemplateFromHtmlHandler
from mailing.html_utils import extract_substitutions, extract_cids


def test_extract_substitutions_finds_vars():
    html = "<p>Hello {fest_name}, welcome to {city}.</p>"
    assert extract_substitutions(html) == {"fest_name", "city"}


def test_extract_substitutions_empty():
    assert extract_substitutions("<p>No vars here</p>") == set()


def test_extract_cids_finds_cids():
    html = '<img src="cid:sinoes"> <img src="cid:band">'
    assert extract_cids(html) == {"sinoes", "band"}


def test_extract_cids_empty():
    assert extract_cids("<p>no cids</p>") == set()


def test_create_template_from_html_saves_template():
    repo = MemoryTemplatesRepo([])
    handler = CreateTemplateFromHtmlHandler(repo)
    handler.execute(CreateTemplateFromHtml(
        subject="Test subject",
        body="<p>Hello</p>",
        substitutions={"fest_name": "nom"},
        images={"sinoes": "mailing/img/sinoes.jpg"},
    ))
    assert len(repo.templates) == 1
    t = repo.templates[0]
    assert t.subject == "Test subject"
    assert t.body == "<p>Hello</p>"
    assert t.substitutions == {"fest_name": "nom"}
    assert t.images == {"sinoes": "mailing/img/sinoes.jpg"}


def test_create_template_generates_uuid():
    repo = MemoryTemplatesRepo([])
    handler = CreateTemplateFromHtmlHandler(repo)
    handler.execute(CreateTemplateFromHtml(
        subject="s", body="b", substitutions={}, images={},
    ))
    assert repo.templates[0].uuid != ""
