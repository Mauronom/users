import uuid as uuid_lib
from dataclasses import dataclass
from hex.investigation.domain import Clue, ClueStatus, ContactForReview, ContactForReviewStatus
from hex.investigation.domain.normalizer import normalize_name


@dataclass
class ExtractContact:
    c_name = "investigation.extract.contact"
    clue_text: str


class ExtractContactHandler:
    def __init__(self, clues_repo, cfr_repo, blacklist_repo, agent):
        self.clues_repo = clues_repo
        self.cfr_repo = cfr_repo
        self.blacklist_repo = blacklist_repo
        self.agent = agent

    def execute(self, cmd):
        clue_obj = self.clues_repo.find_by_clue_text(cmd.clue_text)
        result = self.agent.extract(
            cmd.clue_text,
            summary=clue_obj.summary if clue_obj else "",
            web=clue_obj.web if clue_obj else "",
        )
        print(f"[DEBUG extract handler] result.summary={result.summary!r}")

        if clue_obj:
            clue_obj.status = ClueStatus.done
            clue_obj.summary = result.summary or ""
            self.clues_repo.save(clue_obj)

        status = self._determine_status(result.nom, result.mail)

        cfr = ContactForReview(
            uuid=str(uuid_lib.uuid4()),
            nom=result.nom,
            mail=result.mail,
            web=result.web,
            persona_contacte=result.persona_contacte,
            telefon=result.telefon,
            notes=result.notes,
            idioma=result.idioma,
            source_clue=cmd.clue_text,
            status=status,
        )
        self.cfr_repo.save(cfr)

        self._upsert_new_clues(result.new_clues, cmd.clue_text)

    def _determine_status(self, nom, mail):
        if self.blacklist_repo.is_blacklisted_by_mail(mail):
            return ContactForReviewStatus.rejected
        if self.blacklist_repo.is_blacklisted_by_name(normalize_name(nom)):
            return ContactForReviewStatus.rejected
        if self.cfr_repo.exists_by_mail(mail):
            return ContactForReviewStatus.duplicate
        return ContactForReviewStatus.pending

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
