from .user import User


class CreateUser:
    def __init__(self, init_user_repo):
        self.user_repo = init_user_repo

    def execute(self, uuid, username, email, dni):
        user = User(uuid, username, email, dni)
        self.user_repo.addUser(user)
