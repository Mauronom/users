from .exceptions import InvalidDNI


class User:
    def __init__(self, uuid="", name="", email="", dni=""):
        if (not dni):
            raise InvalidDNI
        self.uuid = uuid
        self.username = name
        self.email = email

        # Verify DNI is not null
        self.dni = dni

    def clone(u):
        return User(u.uuid, u.username, u.email, u.dni)
    
    def __eq__(self, u):
        return self.uuid == u.uuid
