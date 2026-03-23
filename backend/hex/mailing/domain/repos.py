from abc import ABC, abstractmethod


class ContactsRepo(ABC):
    @abstractmethod
    def save(self, contact): pass

    @abstractmethod
    def find_all(self): pass

    @abstractmethod
    def find_by_field(self, field, value): pass


class TemplatesRepo(ABC):
    @abstractmethod
    def save(self, template): pass

    @abstractmethod
    def find_all(self): pass

    @abstractmethod
    def find_by_field(self, field, value): pass


class MailsRepo(ABC):
    @abstractmethod
    def save(self, mail): pass

    @abstractmethod
    def find_all(self): pass

    @abstractmethod
    def find_by_field(self, field, value): pass
