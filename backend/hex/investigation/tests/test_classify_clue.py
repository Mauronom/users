import pytest
from hex.investigation.domain import (
    Clue, ClueStatus, ClueType, ClassifyResult, NewClue, InvestigationAgentPort, ExtractResult,
)
from hex.investigation.infra.repos import MemoryCluesRepo, MemoryContactsForReviewRepo, MemoryBlacklistRepo
from hex.investigation.app.classify_clue import ClassifyClue, ClassifyClueHandler


class FakeAgent(InvestigationAgentPort):
    def __init__(self, classify_result=None, extract_result=None):
        self.classify_calls = []
        self._classify_result = classify_result or ClassifyResult(type="unknown")
        self._extract_result = extract_result

    def classify(self, clue, top_returned):
        self.classify_calls.append((clue, top_returned))
        return self._classify_result

    def extract(self, clue):
        return self._extract_result


def make_clue(text="Xarim Aresté", **kwargs):
    return Clue(clue=text, **kwargs)


def test_classify_sets_type_on_clue():
    clue = make_clue("Xarim Aresté")
    repo = MemoryCluesRepo([clue])
    cfr_repo = MemoryContactsForReviewRepo()
    bl_repo = MemoryBlacklistRepo()
    agent = FakeAgent(ClassifyResult(type="scout"))
    h = ClassifyClueHandler(repo, cfr_repo, bl_repo, agent)
    h.execute(ClassifyClue(clue_text="Xarim Aresté"))

    result = repo.find_by_clue_text("Xarim Aresté")
    assert result.type == ClueType.scout


def test_classify_sets_status_done():
    clue = make_clue("Xarim Aresté")
    repo = MemoryCluesRepo([clue])
    agent = FakeAgent(ClassifyResult(type="scout"))
    h = ClassifyClueHandler(repo, MemoryContactsForReviewRepo(), MemoryBlacklistRepo(), agent)
    h.execute(ClassifyClue(clue_text="Xarim Aresté"))

    assert repo.find_by_clue_text("Xarim Aresté").status == ClueStatus.done


def test_classify_adds_new_clues_as_pending():
    clue = make_clue("Xarim Aresté")
    repo = MemoryCluesRepo([clue])
    agent = FakeAgent(ClassifyResult(type="scout", new_clues=[NewClue("Paupaterres", 7), NewClue("Canet Rock", 4)]))
    h = ClassifyClueHandler(repo, MemoryContactsForReviewRepo(), MemoryBlacklistRepo(), agent)
    h.execute(ClassifyClue(clue_text="Xarim Aresté"))

    new1 = repo.find_by_clue_text("Paupaterres")
    new2 = repo.find_by_clue_text("Canet Rock")
    assert new1 is not None and new1.status == ClueStatus.pending
    assert new2 is not None and new2.status == ClueStatus.pending


def test_classify_new_clue_score_saved():
    clue = make_clue("Xarim Aresté")
    repo = MemoryCluesRepo([clue])
    agent = FakeAgent(ClassifyResult(type="scout", new_clues=[NewClue("Paupaterres", 8)]))
    h = ClassifyClueHandler(repo, MemoryContactsForReviewRepo(), MemoryBlacklistRepo(), agent)
    h.execute(ClassifyClue(clue_text="Xarim Aresté"))

    assert repo.find_by_clue_text("Paupaterres").score == 8


def test_classify_existing_new_clue_increments_times_returned():
    clue = make_clue("Xarim Aresté")
    existing = make_clue("Paupaterres", times_returned=2)
    repo = MemoryCluesRepo([clue, existing])
    agent = FakeAgent(ClassifyResult(type="scout", new_clues=[NewClue("Paupaterres", 7)]))
    h = ClassifyClueHandler(repo, MemoryContactsForReviewRepo(), MemoryBlacklistRepo(), agent)
    h.execute(ClassifyClue(clue_text="Xarim Aresté"))

    assert repo.find_by_clue_text("Paupaterres").times_returned == 3


def test_classify_passes_top_returned_to_agent():
    clue = make_clue("Xarim Aresté")
    top = make_clue("Heliogabal", type=ClueType.entity, times_returned=10)
    repo = MemoryCluesRepo([clue, top])
    agent = FakeAgent(ClassifyResult(type="scout"))
    h = ClassifyClueHandler(repo, MemoryContactsForReviewRepo(), MemoryBlacklistRepo(), agent, top_n=1)
    h.execute(ClassifyClue(clue_text="Xarim Aresté"))

    _, top_returned = agent.classify_calls[0]
    assert "Heliogabal" in top_returned


def test_classify_entity_with_contact_info_creates_contact_for_review():
    clue = make_clue("Paupaterres")
    repo = MemoryCluesRepo([clue])
    cfr_repo = MemoryContactsForReviewRepo()
    agent = FakeAgent(ClassifyResult(
        type="entity", nom="Paupaterres", mail="info@paupaterres.cat",
        web="paupaterres.cat", idioma="ca",
    ))
    h = ClassifyClueHandler(repo, cfr_repo, MemoryBlacklistRepo(), agent)
    h.execute(ClassifyClue(clue_text="Paupaterres"))

    assert cfr_repo.exists_by_mail("info@paupaterres.cat")


def test_classify_saves_summary_to_clue():
    clue = make_clue("Xarim Aresté")
    repo = MemoryCluesRepo([clue])
    agent = FakeAgent(ClassifyResult(type="scout", summary="Cantautor català del circuit indie"))
    h = ClassifyClueHandler(repo, MemoryContactsForReviewRepo(), MemoryBlacklistRepo(), agent)
    h.execute(ClassifyClue(clue_text="Xarim Aresté"))

    assert repo.find_by_clue_text("Xarim Aresté").summary == "Cantautor català del circuit indie"


def test_classify_saves_web_to_clue():
    clue = make_clue("Paupaterres")
    repo = MemoryCluesRepo([clue])
    agent = FakeAgent(ClassifyResult(type="entity", web="paupaterres.cat"))
    h = ClassifyClueHandler(repo, MemoryContactsForReviewRepo(), MemoryBlacklistRepo(), agent)
    h.execute(ClassifyClue(clue_text="Paupaterres"))

    assert repo.find_by_clue_text("Paupaterres").web == "paupaterres.cat"


def test_classify_entity_duplicate_mail_not_added_twice():
    from hex.investigation.domain import ContactForReview
    clue = make_clue("Paupaterres")
    existing_cfr = ContactForReview(uuid="x", nom="Paupaterres", mail="info@paupaterres.cat")
    repo = MemoryCluesRepo([clue])
    cfr_repo = MemoryContactsForReviewRepo([existing_cfr])
    agent = FakeAgent(ClassifyResult(
        type="entity", nom="Paupaterres", mail="info@paupaterres.cat",
    ))
    h = ClassifyClueHandler(repo, cfr_repo, MemoryBlacklistRepo(), agent)
    h.execute(ClassifyClue(clue_text="Paupaterres"))

    assert len(cfr_repo.contacts) == 1
