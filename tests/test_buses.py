from app import GetUsers,GetUsersHandler
from infra import MemoryUsersRepo, QueryBus
from domain import User

def test_buses_1():
    u = User('1', 'u1', 'u1@test.com', '12345678A')
    repo_user = MemoryUsersRepo([u])
    h = GetUsersHandler(repo_user)
    q = GetUsers()
    q_bus = QueryBus()
    q_bus.subscribe(GetUsers,h)
    
    users = q_bus.dispatch(q)
    assert len(users) == 1
    assert users[0] == u
