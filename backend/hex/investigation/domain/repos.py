from abc import ABC, abstractmethod


class CluesRepo(ABC):
    @abstractmethod
    def save(self, clue): pass

    @abstractmethod
    def find_all(self): pass

    @abstractmethod
    def find_by_field(self, field, value): pass

    @abstractmethod
    def find_pending(self): pass

    @abstractmethod
    def find_top_returned(self, n): pass

    @abstractmethod
    def find_by_clue_text(self, clue_text): pass


class ContactsForReviewRepo(ABC):
    @abstractmethod
    def save(self, contact): pass

    @abstractmethod
    def find_all(self): pass

    @abstractmethod
    def find_by_field(self, field, value): pass

    @abstractmethod
    def exists_by_mail(self, mail): pass


class BlacklistRepo(ABC):
    @abstractmethod
    def save(self, entry): pass

    @abstractmethod
    def find_all(self): pass

    @abstractmethod
    def is_blacklisted_by_mail(self, mail): pass

    @abstractmethod
    def is_blacklisted_by_name(self, normalized_name): pass
