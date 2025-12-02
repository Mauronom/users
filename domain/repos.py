from abc import abstractmethod
from . import User
from typing import List


class UsersRepo:

    @abstractmethod
    def save(self, user): ...

    @abstractmethod
    def find_all(self) -> List["User"]: ...

    @abstractmethod
    def find_by_field(self, field, value) -> List["User"]: ...
