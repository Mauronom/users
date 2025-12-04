class GetUsers:
    q_name='get.users'

class GetUsersHandler:
    def __init__(self, init_user_repo):
        self.user_repo = init_user_repo

    def execute(self):
        return self.user_repo.find_all()