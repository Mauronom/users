from abc import ABC, abstractmethod


class MailSenderPort(ABC):
    @abstractmethod
    def send(self, mail) -> None:
        pass


class CidImageRepoPort(ABC):
    @abstractmethod
    def find(self, cid_name: str) -> bytes:
        pass


class AttachmentRepoPort(ABC):
    @abstractmethod
    def find(self, path: str) -> tuple:
        """Returns (filename, bytes)."""
        pass
