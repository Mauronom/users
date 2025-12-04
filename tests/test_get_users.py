from infra import MemoryUsersRepo
from app import GetUsers, GetUsersHandler
from domain import User
from infra import QueryBus


def test_get_users_1():
    q_bus = QueryBus()
    repo_user = MemoryUsersRepo([])
    h = GetUsersHandler(repo_user)
    q = GetUsers()
    q_bus.subscribe(GetUsers,h)
    users = q_bus.dispatch(q)
    assert len(users) == 0
    
def test_get_users_2():
    q_bus = QueryBus()
    u = User('1', 'u1', 'u1@test.com', '12345678A')
    repo_user = MemoryUsersRepo([u])
    h = GetUsersHandler(repo_user)
    q = GetUsers()
    q_bus.subscribe(GetUsers,h)
    users = q_bus.dispatch(q)
    assert len(users) == 1
    assert users[0] == u

