class BlacklistEntry:
    def __init__(self, normalized_name="", mail=""):
        if not normalized_name and not mail:
            raise ValueError("at least one of normalized_name or mail must be set")
        self.normalized_name = normalized_name
        self.mail = mail

    def clone(self):
        return BlacklistEntry(self.normalized_name, self.mail)
