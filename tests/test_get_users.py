from infra import MemoryUsersRepo
from app import GetUsers
from domain import User
from domain import UsernameAlreadyExists
from domain import EmailAlreadyExists
from domain import DNIAlreadyExists
from domain import InvalidDNI


def test_get_users_1():
    repo_user = MemoryUsersRepo([])
    cmd = GetUsers(repo_user)
    users = cmd.execute()
    assert len(users) == 0
    
def test_get_users_2():
    u = User('1', 'u1', 'u1@test.com', '12345678A')
    repo_user = MemoryUsersRepo([u])
    cmd = GetUsers(repo_user)
    users = cmd.execute()
    assert len(users) == 1
    assert users[0] == u

