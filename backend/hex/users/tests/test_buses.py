from hex.users.app import GetUsers, GetUsersHandler, CreateUser, CreateUserHandler
from hex.users.infra import MemoryUsersRepo, QueryBus, CommandBus
from hex.users.domain import User

def test_buses_1():
    u = User('1', 'u1', 'u1@test.com', '12345678A')
    repo_user = MemoryUsersRepo([u])
    h = GetUsersHandler(repo_user)
    q = GetUsers()
    q_bus = QueryBus()
    q_bus.subscribe(GetUsers, h)

    users = q_bus.dispatch(q)
    assert len(users) == 1
    assert users[0] == u

def test_buses_2():
    u = User('1', 'u1', 'u1@test.com', '12345678A')
    repo_user = MemoryUsersRepo([])
    h = CreateUserHandler(repo_user)
    c = CreateUser("1","u1","u1@test.com","12345678A")
    c_bus = CommandBus()
    c_bus.subscribe(CreateUser, h)
    
    ok = c_bus.dispatch(c)
    assert ok == "ok"

    users = repo_user.find_all()
    assert len(users) == 1
    assert users[0] == u
    assert users[0].username == u.username
    assert users[0].email == u.email
    assert users[0].dni == u.dni

