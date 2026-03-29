from dataclasses import dataclass
from hex.investigation.domain import ContactForReviewStatus, DuplicateContact
from hex.mailing.domain import Contact
import uuid as uuid_lib


@dataclass
class ApproveContact:
    c_name = "investigation.approve.contact"
    contact_for_review_uuid: str


class ApproveContactHandler:
    def __init__(self, cfr_repo, contacts_repo):
        self.cfr_repo = cfr_repo
        self.contacts_repo = contacts_repo

    def execute(self, cmd):
        cfrs = self.cfr_repo.find_by_field("uuid", cmd.contact_for_review_uuid)
        cfr = cfrs[0]

        existing = self.contacts_repo.find_by_field("mail", cfr.mail)
        if existing:
            raise DuplicateContact(f"mail {cfr.mail} already in contacts")

        contact = Contact(
            uuid=str(uuid_lib.uuid4()),
            nom=cfr.nom,
            mail=cfr.mail,
            web=cfr.web,
            persona_contacte=cfr.persona_contacte,
            telefon=cfr.telefon,
            notes=cfr.notes,
            idioma=cfr.idioma,
        )
        self.contacts_repo.save(contact)

        cfr.status = ContactForReviewStatus.approved
        self.cfr_repo.save(cfr)
