class Contact:
    def __init__(self, uuid="", nom="", mail="", web="", persona_contacte="", telefon="", notes="", data_enviat=None, idioma=""):
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
        self.data_enviat = data_enviat
        self.idioma = idioma

    def clone(self):
        return Contact(self.uuid, self.nom, self.mail, self.web, self.persona_contacte, self.telefon, self.notes, self.data_enviat, self.idioma)

    def __eq__(self, other):
        return self.uuid == other.uuid

    def to_primitive(self):
        return {"uuid": self.uuid, "nom": self.nom, "mail": self.mail, "web": self.web, "persona_contacte": self.persona_contacte, "telefon": self.telefon, "notes": self.notes, "data_enviat": self.data_enviat, "idioma": self.idioma}
