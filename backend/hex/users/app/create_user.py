from hex.users.domain import User
from hex.users.domain import UsernameAlreadyExists
from hex.users.domain import EmailAlreadyExists
from hex.users.domain import DNIAlreadyExists


class CreateUser:
       c_name = "create.user"


class CreateUserHandler:
    def __init__(self, init_user_repo):
        self.user_repo = init_user_repo

    def execute(self, user_info):

        uuid = user_info["uuid"]
        username = user_info["username"]
        email = user_info["email"]
        dni = user_info["dni"]
        
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

        return "ok"
