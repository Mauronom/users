from domain import User
from domain import UsernameAlreadyExists
from domain import EmailAlreadyExists
from domain import DNIAlreadyExists


class CreateUser:
    def __init__(self, init_user_repo):
        self.user_repo = init_user_repo

    def execute(self, uuid, username, email, dni):
        user = User(uuid, username, email, dni)

        # Check username duplicates
        duplicates = self.user_repo.find_by_field("username", username)
        if duplicates:
            raise UsernameAlreadyExists()

        # Check email duplicates
        duplicates = self.user_repo.find_by_field("email", email)
        if duplicates:
            raise EmailAlreadyExists()

        # Check DNI duplicates
        duplicates = self.user_repo.find_by_field("dni", dni)
        if duplicates:
            raise DNIAlreadyExists()

        self.user_repo.save(user)
