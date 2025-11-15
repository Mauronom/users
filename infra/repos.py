class MemoryUsersRepo:
    def __init__(self, init_users):
        self.users = init_users

    def addUser(self, user):
        self.users.append(user)

    def find_all(self):
        ret = self.users.copy()
        return ret
