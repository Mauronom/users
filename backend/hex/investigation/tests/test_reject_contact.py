from hex.investigation.domain import ContactForReview, ContactForReviewStatus
from hex.investigation.infra.repos import MemoryContactsForReviewRepo, MemoryBlacklistRepo
from hex.investigation.app.reject_contact import RejectContact, RejectContactHandler


def make_cfr(**kwargs):
    defaults = dict(uuid="cfr1", nom="Apolo", mail="info@apolo.cat")
    defaults.update(kwargs)
    return ContactForReview(**defaults)


def test_reject_sets_status_rejected():
    cfr = make_cfr()
    cfr_repo = MemoryContactsForReviewRepo([cfr])
    h = RejectContactHandler(cfr_repo, MemoryBlacklistRepo())
    h.execute(RejectContact(contact_for_review_uuid="cfr1"))

    result = cfr_repo.find_by_field("uuid", "cfr1")[0]
    assert result.status == ContactForReviewStatus.rejected


def test_reject_without_blacklist_does_not_add_to_blacklist():
    cfr = make_cfr()
    cfr_repo = MemoryContactsForReviewRepo([cfr])
    bl_repo = MemoryBlacklistRepo()
    h = RejectContactHandler(cfr_repo, bl_repo)
    h.execute(RejectContact(contact_for_review_uuid="cfr1"))

    assert len(bl_repo.entries) == 0


def test_reject_with_blacklist_adds_blacklist_entry():
    cfr = make_cfr()
    cfr_repo = MemoryContactsForReviewRepo([cfr])
    bl_repo = MemoryBlacklistRepo()
    h = RejectContactHandler(cfr_repo, bl_repo)
    h.execute(RejectContact(contact_for_review_uuid="cfr1", blacklist=True))

    assert bl_repo.is_blacklisted_by_mail("info@apolo.cat")


def test_reject_with_blacklist_stores_normalized_name():
    cfr = make_cfr(nom="Sala Apolo")
    cfr_repo = MemoryContactsForReviewRepo([cfr])
    bl_repo = MemoryBlacklistRepo()
    h = RejectContactHandler(cfr_repo, bl_repo)
    h.execute(RejectContact(contact_for_review_uuid="cfr1", blacklist=True))

    assert bl_repo.is_blacklisted_by_name("apolo")
