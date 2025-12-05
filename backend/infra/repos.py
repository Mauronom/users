from domain import UsersRepo


class MemoryUsersRepo(UsersRepo):
    def __init__(self, init_users):
        self.users = init_users

    def save(self, user):
        self.users.append(user.clone())

    def find_all(self):
        res = []
        for u in self.users:
            res.append(u.clone())
        return res

    def find_by_field(self, field, value):
        res = []
        for u in self.users:
            if (getattr(u, field) == value):
                res.append(u)
        return res
