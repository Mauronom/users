from abc import ABC, abstractmethod


class MailSenderPort(ABC):
    @abstractmethod
    def send(self, mail) -> None:
        pass
