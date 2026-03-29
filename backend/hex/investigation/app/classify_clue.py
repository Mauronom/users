import uuid as uuid_lib
from dataclasses import dataclass
from hex.investigation.domain import Clue, ClueStatus, ClueType, ContactForReview, ContactForReviewStatus


@dataclass
class ClassifyClue:
    c_name = "investigation.classify.clue"
    clue_text: str


class ClassifyClueHandler:
    def __init__(self, clues_repo, cfr_repo, blacklist_repo, agent, top_n=20):
        self.clues_repo = clues_repo
        self.cfr_repo = cfr_repo
        self.blacklist_repo = blacklist_repo
        self.agent = agent
        self.top_n = top_n

    def execute(self, cmd):
        top_returned = [c.clue for c in self.clues_repo.find_top_returned(self.top_n)]
        result = self.agent.classify(cmd.clue_text, top_returned)

        clue = self.clues_repo.find_by_clue_text(cmd.clue_text)
        clue.type = ClueType(result.type) if result.type in ClueType._value2member_map_ else ClueType.unknown
        clue.status = ClueStatus.done
        self.clues_repo.save(clue)

        self._upsert_new_clues(result.new_clues, cmd.clue_text)

        if clue.type == ClueType.entity and result.mail and not self.cfr_repo.exists_by_mail(result.mail):
            self._save_contact_for_review(result, cmd.clue_text)

    def _upsert_new_clues(self, new_clues, source_clue_text):
        for item in new_clues:
            existing = self.clues_repo.find_by_clue_text(item.clue)
            if existing:
                existing.times_returned += 1
                self.clues_repo.save(existing)
            else:
                self.clues_repo.save(Clue(
                    clue=item.clue,
                    status=ClueStatus.pending,
                    score=item.score,
                    source_clue=source_clue_text,
                ))

    def _save_contact_for_review(self, result, source_clue_text):
        cfr = ContactForReview(
            uuid=str(uuid_lib.uuid4()),
            nom=result.nom,
            mail=result.mail,
            web=result.web or "",
            persona_contacte=result.persona_contacte or "",
            telefon=result.telefon or "",
            notes=result.notes or "",
            idioma=result.idioma or "",
            source_clue=source_clue_text,
            status=ContactForReviewStatus.pending,
        )
        self.cfr_repo.save(cfr)
