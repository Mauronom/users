from domain import User
from domain import UsernameAlreadyExists
from domain import EmailAlreadyExists
from domain import DNIAlreadyExists


class GetUsers:
    def __init__(self, init_user_repo):
        self.user_repo = init_user_repo

    def execute(self):
        return self.user_repo.find_all()