from dataclasses import dataclass

@dataclass
class GetUserInfo:
    q_name = "GetUserInfo"
    username:str
class GetUserInfoHandler:
    def __init__(self, init_user_repo):
        self.user_repo = init_user_repo

    def execute(self, q):
        res = self.user_repo.find_by_field("username",q.username)
        if (res == []):
            return None
        else:
            return res[0]
