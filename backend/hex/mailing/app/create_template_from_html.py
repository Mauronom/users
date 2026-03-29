import uuid as uuid_lib
from dataclasses import dataclass, field
from hex.mailing.domain import Template


@dataclass
class CreateTemplateFromHtml:
    c_name = "create.template_from_html"
    subject: str
    body: str
    substitutions: dict = field(default_factory=dict)
    images: dict = field(default_factory=dict)


class CreateTemplateFromHtmlHandler:
    def __init__(self, templates_repo):
        self.templates_repo = templates_repo

    def execute(self, cmd):
        template = Template(
            uuid=str(uuid_lib.uuid4()),
            subject=cmd.subject,
            body=cmd.body,
            substitutions=cmd.substitutions,
            attachments=[],
            images=cmd.images,
        )
        self.templates_repo.save(template)
        return "ok"
