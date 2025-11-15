class MemoryUsersRepo:
    def __init__(self, users):
        self.users = users

    def save(self, user):
        self.users.append(user)

    def find_all(self):
        return self.users.copy()