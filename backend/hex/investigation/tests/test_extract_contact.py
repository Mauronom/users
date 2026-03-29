from hex.investigation.domain import (
    Clue, ClueType, ContactForReview, ContactForReviewStatus, BlacklistEntry,
    ClassifyResult, ExtractResult, NewClue, InvestigationAgentPort,
)
from hex.investigation.infra.repos import MemoryCluesRepo, MemoryContactsForReviewRepo, MemoryBlacklistRepo
from hex.investigation.app.extract_contact import ExtractContact, ExtractContactHandler


class FakeAgent(InvestigationAgentPort):
    def __init__(self, extract_result=None):
        self._result = extract_result or ExtractResult(nom="Paupaterres", mail="info@paupaterres.cat")

    def classify(self, clue, top_returned): pass

    def extract(self, clue):
        return self._result


def make_entity_clue(text="Paupaterres"):
    return Clue(clue=text, type=ClueType.entity)


def test_extract_creates_contact_for_review():
    repo = MemoryCluesRepo([make_entity_clue()])
    cfr_repo = MemoryContactsForReviewRepo()
    h = ExtractContactHandler(repo, cfr_repo, MemoryBlacklistRepo(), FakeAgent())
    h.execute(ExtractContact(clue_text="Paupaterres"))

    assert cfr_repo.exists_by_mail("info@paupaterres.cat")


def test_extract_contact_status_is_pending():
    repo = MemoryCluesRepo([make_entity_clue()])
    cfr_repo = MemoryContactsForReviewRepo()
    h = ExtractContactHandler(repo, cfr_repo, MemoryBlacklistRepo(), FakeAgent())
    h.execute(ExtractContact(clue_text="Paupaterres"))

    contacts = cfr_repo.find_all()
    assert contacts[0].status == ContactForReviewStatus.pending


def test_extract_duplicate_mail_marked_duplicate():
    existing = ContactForReview(uuid="x", nom="Paupaterres", mail="info@paupaterres.cat")
    repo = MemoryCluesRepo([make_entity_clue()])
    cfr_repo = MemoryContactsForReviewRepo([existing])
    h = ExtractContactHandler(repo, cfr_repo, MemoryBlacklistRepo(), FakeAgent())
    h.execute(ExtractContact(clue_text="Paupaterres"))

    dupes = cfr_repo.find_by_field("status", ContactForReviewStatus.duplicate)
    assert len(dupes) == 1


def test_extract_blacklisted_mail_marked_rejected():
    bl_repo = MemoryBlacklistRepo([BlacklistEntry(mail="info@paupaterres.cat")])
    repo = MemoryCluesRepo([make_entity_clue()])
    cfr_repo = MemoryContactsForReviewRepo()
    h = ExtractContactHandler(repo, cfr_repo, bl_repo, FakeAgent())
    h.execute(ExtractContact(clue_text="Paupaterres"))

    rejected = cfr_repo.find_by_field("status", ContactForReviewStatus.rejected)
    assert len(rejected) == 1


def test_extract_blacklisted_name_marked_rejected():
    bl_repo = MemoryBlacklistRepo([BlacklistEntry(normalized_name="paupaterres")])
    repo = MemoryCluesRepo([make_entity_clue()])
    cfr_repo = MemoryContactsForReviewRepo()
    h = ExtractContactHandler(repo, cfr_repo, bl_repo, FakeAgent())
    h.execute(ExtractContact(clue_text="Paupaterres"))

    rejected = cfr_repo.find_by_field("status", ContactForReviewStatus.rejected)
    assert len(rejected) == 1


def test_extract_new_clues_upserted():
    agent = FakeAgent(ExtractResult(
        nom="Paupaterres", mail="info@paupaterres.cat",
        new_clues=[NewClue("La Mirona", 6)],
    ))
    repo = MemoryCluesRepo([make_entity_clue()])
    h = ExtractContactHandler(repo, MemoryContactsForReviewRepo(), MemoryBlacklistRepo(), agent)
    h.execute(ExtractContact(clue_text="Paupaterres"))

    assert repo.find_by_clue_text("La Mirona") is not None


def test_extract_source_clue_recorded():
    repo = MemoryCluesRepo([make_entity_clue()])
    cfr_repo = MemoryContactsForReviewRepo()
    h = ExtractContactHandler(repo, cfr_repo, MemoryBlacklistRepo(), FakeAgent())
    h.execute(ExtractContact(clue_text="Paupaterres"))

    contacts = cfr_repo.find_all()
    assert contacts[0].source_clue == "Paupaterres"
