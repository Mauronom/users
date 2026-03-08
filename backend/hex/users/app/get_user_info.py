class GetUserInfo:
    q_name = "GetUserInfo"

class GetUserInfoHandler:
    def __init__(self, init_user_repo):
        self.user_repo = init_user_repo

    def execute(self, param):
        res = self.user_repo.find_by_field("username",param["username"])
        if (res == []):
            return None
        else:
            return res[0]
