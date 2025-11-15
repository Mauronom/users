from domain import User

class CreateUser:
    def __init__(self, repo):
        self.repo = repo

    def execute(self, uuid, username, email, dni):
        user = User(uuid, username, email, dni)
        self.repo.save(user)