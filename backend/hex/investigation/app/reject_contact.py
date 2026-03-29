from dataclasses import dataclass
from hex.investigation.domain import ContactForReviewStatus, BlacklistEntry
from hex.investigation.domain.normalizer import normalize_name


@dataclass
class RejectContact:
    c_name = "investigation.reject.contact"
    contact_for_review_uuid: str
    blacklist: bool = False


class RejectContactHandler:
    def __init__(self, cfr_repo, blacklist_repo):
        self.cfr_repo = cfr_repo
        self.blacklist_repo = blacklist_repo

    def execute(self, cmd):
        cfrs = self.cfr_repo.find_by_field("uuid", cmd.contact_for_review_uuid)
        cfr = cfrs[0]

        cfr.status = ContactForReviewStatus.rejected
        self.cfr_repo.save(cfr)

        if cmd.blacklist:
            self.blacklist_repo.save(BlacklistEntry(
                normalized_name=normalize_name(cfr.nom),
                mail=cfr.mail,
            ))
