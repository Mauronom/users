from .exceptions import InvalidDNI


class User:
    def __init__(self, uuid="", username="", email="", dni=""):
        if (not dni):
            raise InvalidDNI
        self.uuid = uuid
        self.username = username
        self.email = email

        # Verify DNI is not null
        self.dni = dni

    def clone(u):
        return User(u.uuid, u.username, u.email, u.dni)
    
    def __eq__(self, u):
        return self.uuid == u.uuid
    
    def __str__(self,):
        return f"{self.uuid}-{self.username}-{self.email}-{self.dni}"
    
    def to_primitive(self):
        return {'uuid':self.uuid,
                'username': self.username,
                'email': self.email,
                'dni':self.dni}
