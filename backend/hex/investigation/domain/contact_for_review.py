from enum import Enum


class ContactForReviewStatus(Enum):
    pending = "pending"
    approved = "approved"
    rejected = "rejected"
    duplicate = "duplicate"


class ContactForReview:
    def __init__(self, uuid, nom, mail, web="", persona_contacte="", telefon="",
                 notes="", idioma="", tags="", source_clue="",
                 status=ContactForReviewStatus.pending):
        if not nom:
            raise ValueError("nom cannot be empty")
        if not mail:
            raise ValueError("mail cannot be empty")
        self.uuid = uuid
        self.nom = nom
        self.mail = mail
        self.web = web
        self.persona_contacte = persona_contacte
        self.telefon = telefon
        self.notes = notes
        self.idioma = idioma
        self.tags = tags
        self.source_clue = source_clue
        self.status = status

    def clone(self):
        return ContactForReview(
            self.uuid, self.nom, self.mail, self.web, self.persona_contacte,
            self.telefon, self.notes, self.idioma, self.tags,
            self.source_clue, self.status,
        )

    def __eq__(self, other):
        return self.uuid == other.uuid
