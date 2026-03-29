import pytest
from hex.investigation.domain import (
    ContactForReview, ContactForReviewStatus, DuplicateContact,
)
from hex.mailing.domain import Contact
from hex.mailing.infra.repos import MemoryContactsRepo
from hex.investigation.infra.repos import MemoryContactsForReviewRepo
from hex.investigation.app.approve_contact import ApproveContact, ApproveContactHandler


def make_cfr(**kwargs):
    defaults = dict(uuid="cfr1", nom="Paupaterres", mail="info@paupaterres.cat")
    defaults.update(kwargs)
    return ContactForReview(**defaults)


def test_approve_creates_contact_in_contacts_repo():
    cfr = make_cfr()
    cfr_repo = MemoryContactsForReviewRepo([cfr])
    contacts_repo = MemoryContactsRepo([])
    h = ApproveContactHandler(cfr_repo, contacts_repo)
    h.execute(ApproveContact(contact_for_review_uuid="cfr1"))

    contacts = contacts_repo.find_by_field("mail", "info@paupaterres.cat")
    assert len(contacts) == 1
    assert contacts[0].nom == "Paupaterres"


def test_approve_sets_status_approved():
    cfr = make_cfr()
    cfr_repo = MemoryContactsForReviewRepo([cfr])
    h = ApproveContactHandler(cfr_repo, MemoryContactsRepo([]))
    h.execute(ApproveContact(contact_for_review_uuid="cfr1"))

    result = cfr_repo.find_by_field("uuid", "cfr1")[0]
    assert result.status == ContactForReviewStatus.approved


def test_approve_raises_duplicate_if_mail_in_contacts_repo():
    existing = Contact(uuid="c1", nom="Paupaterres", mail="info@paupaterres.cat")
    cfr = make_cfr()
    cfr_repo = MemoryContactsForReviewRepo([cfr])
    contacts_repo = MemoryContactsRepo([existing])
    h = ApproveContactHandler(cfr_repo, contacts_repo)

    with pytest.raises(DuplicateContact):
        h.execute(ApproveContact(contact_for_review_uuid="cfr1"))
