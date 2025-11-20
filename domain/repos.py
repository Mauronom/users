from abc import abstractmethod
from . import User


class UsersRepo:

    @abstractmethod
    def save(self, user): ...

    @abstractmethod
    def find_all(self) -> list["User"]: ...

    @abstractmethod
    def find_by_field(self, field, value) -> list["User"]: ...
