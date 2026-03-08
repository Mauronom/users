
from hex.users.infra import MemoryUsersRepo, QueryBus
from hex.users.app import GetUserInfo, GetUserInfoHandler
from hex.users.domain import User


def test_if_user_doesnt_exist_returns_none():
    q_bus = QueryBus()
    repo_user = MemoryUsersRepo([])
    h = GetUserInfoHandler(repo_user)
    q = GetUserInfo()
    q_bus.subscribe(GetUserInfo,h)
    param = {"username" : "u1"}
    user = q_bus.dispatch(q.q_name, param)

    assert user == None

def test_if_user_exists_returns_right_user():
    q_bus = QueryBus()
    u1 = User("1","u1","u1@test.com","12345678A")
    repo_user = MemoryUsersRepo([u1])
    h = GetUserInfoHandler(repo_user)
    q = GetUserInfo()
    q_bus.subscribe(GetUserInfo,h)
    param = {"username" : "u1"}
    returned_user = q_bus.dispatch(q.q_name, param)

    assert returned_user.uuid == u1.uuid
    assert returned_user.username == u1.username
    assert returned_user.email == u1.email
    assert returned_user.dni == u1.dni
