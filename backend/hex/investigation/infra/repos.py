from hex.investigation.domain import (
    CluesRepo, ContactsForReviewRepo, BlacklistRepo,
    ClueStatus, ClueType,
)


class MemoryCluesRepo(CluesRepo):
    def __init__(self, init_clues=None):
        self.clues = list(init_clues or [])

    def save(self, clue):
        for i, c in enumerate(self.clues):
            if c.clue == clue.clue:
                self.clues[i] = clue.clone()
                return
        self.clues.append(clue.clone())

    def find_all(self):
        return [c.clone() for c in self.clues]

    def find_by_field(self, field, value):
        return [c.clone() for c in self.clues if getattr(c, field) == value]

    def find_pending(self):
        return [c.clone() for c in self.clues if c.status == ClueStatus.pending]

    def find_top_returned(self, n):
        entities = [c for c in self.clues if c.type == ClueType.entity]
        entities.sort(key=lambda c: c.times_returned, reverse=True)
        return [c.clone() for c in entities[:n]]

    def find_by_clue_text(self, clue_text):
        matches = [c for c in self.clues if c.clue == clue_text]
        return matches[0].clone() if matches else None


class MemoryContactsForReviewRepo(ContactsForReviewRepo):
    def __init__(self, init_contacts=None):
        self.contacts = list(init_contacts or [])

    def save(self, contact):
        for i, c in enumerate(self.contacts):
            if c.uuid == contact.uuid:
                self.contacts[i] = contact.clone()
                return
        self.contacts.append(contact.clone())

    def find_all(self):
        return [c.clone() for c in self.contacts]

    def find_by_field(self, field, value):
        return [c.clone() for c in self.contacts if getattr(c, field) == value]

    def exists_by_mail(self, mail):
        return any(c.mail == mail for c in self.contacts)


class MemoryBlacklistRepo(BlacklistRepo):
    def __init__(self, init_entries=None):
        self.entries = list(init_entries or [])

    def save(self, entry):
        self.entries.append(entry.clone())

    def find_all(self):
        return [e.clone() for e in self.entries]

    def is_blacklisted_by_mail(self, mail):
        return any(e.mail == mail for e in self.entries if e.mail)

    def is_blacklisted_by_name(self, normalized_name):
        return any(e.normalized_name == normalized_name for e in self.entries if e.normalized_name)


class DjangoCluesRepo(CluesRepo):
    def save(self, clue):
        from investigation.models import ClueModel
        print(f"[DEBUG repo.save] clue={clue.clue!r} summary={clue.summary!r}")
        ClueModel.objects.update_or_create(
            clue=clue.clue,
            defaults={
                "status": clue.status.value,
                "type": clue.type.value,
                "score": clue.score,
                "source_clue_text": clue.source_clue,
                "times_returned": clue.times_returned,
                "summary": clue.summary,
                "web": clue.web,
            },
        )

    def find_all(self):
        from investigation.models import ClueModel
        return [self._to_domain(c) for c in ClueModel.objects.all()]

    def find_by_field(self, field, value):
        from investigation.models import ClueModel
        return [self._to_domain(c) for c in ClueModel.objects.filter(**{field: value})]

    def find_pending(self):
        from investigation.models import ClueModel
        return [self._to_domain(c) for c in ClueModel.objects.filter(status="pending")]

    def find_top_returned(self, n):
        from investigation.models import ClueModel
        qs = ClueModel.objects.filter(type="entity").order_by("-times_returned")[:n]
        return [self._to_domain(c) for c in qs]

    def find_by_clue_text(self, clue_text):
        from investigation.models import ClueModel
        obj = ClueModel.objects.filter(clue=clue_text).first()
        return self._to_domain(obj) if obj else None

    def _to_domain(self, obj):
        from hex.investigation.domain import Clue, ClueStatus, ClueType
        return Clue(
            clue=obj.clue,
            status=ClueStatus(obj.status),
            type=ClueType(obj.type),
            score=obj.score,
            source_clue=obj.source_clue_text or "",
            times_returned=obj.times_returned,
            summary=obj.summary or "",
            web=obj.web or "",
        )


class DjangoContactsForReviewRepo(ContactsForReviewRepo):
    def save(self, contact):
        from investigation.models import ContactForReviewModel
        ContactForReviewModel.objects.update_or_create(
            uuid=contact.uuid,
            defaults={
                "nom": contact.nom, "mail": contact.mail, "web": contact.web,
                "persona_contacte": contact.persona_contacte, "telefon": contact.telefon,
                "notes": contact.notes, "idioma": contact.idioma, "tags": contact.tags,
                "source_clue": contact.source_clue, "status": contact.status.value,
            },
        )

    def find_all(self):
        from investigation.models import ContactForReviewModel
        return [self._to_domain(c) for c in ContactForReviewModel.objects.all()]

    def find_by_field(self, field, value):
        from investigation.models import ContactForReviewModel
        return [self._to_domain(c) for c in ContactForReviewModel.objects.filter(**{field: value})]

    def exists_by_mail(self, mail):
        from investigation.models import ContactForReviewModel
        return ContactForReviewModel.objects.filter(mail=mail).exists()

    def _to_domain(self, obj):
        from hex.investigation.domain import ContactForReview, ContactForReviewStatus
        return ContactForReview(
            uuid=str(obj.uuid), nom=obj.nom, mail=obj.mail, web=obj.web,
            persona_contacte=obj.persona_contacte, telefon=obj.telefon,
            notes=obj.notes, idioma=obj.idioma, tags=obj.tags,
            source_clue=obj.source_clue, status=ContactForReviewStatus(obj.status),
        )


class DjangoBlacklistRepo(BlacklistRepo):
    def save(self, entry):
        from investigation.models import BlacklistModel
        BlacklistModel.objects.create(
            normalized_name=entry.normalized_name,
            mail=entry.mail,
        )

    def find_all(self):
        from investigation.models import BlacklistModel
        return [self._to_domain(e) for e in BlacklistModel.objects.all()]

    def is_blacklisted_by_mail(self, mail):
        from investigation.models import BlacklistModel
        return BlacklistModel.objects.filter(mail=mail).exists()

    def is_blacklisted_by_name(self, normalized_name):
        from investigation.models import BlacklistModel
        return BlacklistModel.objects.filter(normalized_name=normalized_name).exists()

    def _to_domain(self, obj):
        from hex.investigation.domain import BlacklistEntry
        return BlacklistEntry(normalized_name=obj.normalized_name, mail=obj.mail)
