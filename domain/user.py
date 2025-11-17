class User:
    def __init__(self, uuid="", name="", email="", dni=""):
        self.uuid = uuid
        self.username = name
        self.email = email
        self.dni = dni

    def clone(u):
        return User(u.uuid,u.username,u.email,u.dni)
