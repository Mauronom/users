from infra import MemoryUsersRepo
from app import GetUsersHandler
from domain import User



def test_get_users_1():
    repo_user = MemoryUsersRepo([])
    cmd = GetUsersHandler(repo_user)
    users = cmd.execute()
    assert len(users) == 0
    
def test_get_users_2():
    u = User('1', 'u1', 'u1@test.com', '12345678A')
    repo_user = MemoryUsersRepo([u])
    cmd = GetUsersHandler(repo_user)
    users = cmd.execute()
    assert len(users) == 1
    assert users[0] == u

