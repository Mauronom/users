from hex.users.infra import MemoryUsersRepo, CommandBus
from hex.users.app import CreateUser, CreateUserHandler
from hex.users.domain import User
from hex.users.domain import UsernameAlreadyExists
from hex.users.domain import EmailAlreadyExists
from hex.users.domain import DNIAlreadyExists
from hex.users.domain import InvalidDNI


def test_create_user_1():
    c_bus = CommandBus()
    repo_user = MemoryUsersRepo([])
    h = CreateUserHandler(repo_user)
    c = CreateUser()
    c_bus.subscribe(CreateUser,h)
    user_info = {
        "uuid": "aaaaa11111",
        "username": "username1",
        "email": "email@test.com",
        "dni": "12345678A"
    }
    c_bus.dispatch(c.c_name, user_info)

    users = repo_user.users
    assert len(users) == 1
    u = users[0]
    assert u.uuid == 'aaaaa11111'
    assert u.username == 'username1'
    assert u.email == 'email@test.com'
    assert u.dni == '12345678A'


def test_create_user_2():
    repo_user = MemoryUsersRepo([User('1', 'u1', 'u1@test.com', '12345678A')])
    c_bus = CommandBus()
    h = CreateUserHandler(repo_user)
    c = CreateUser()
    c_bus.subscribe(CreateUser,h)
    user_info = {
        "uuid": "1",
        "username": "u1",
        "email": "u1@test.com",
        "dni": "12345678A"
    }
    try:
        c_bus.dispatch(c.c_name, user_info)
        users = repo_user.users
    except Exception as e:
        assert type(e) == UsernameAlreadyExists
    else:
        assert False
    users = repo_user.find_all()
    assert len(users) == 1
    u = users[0]
    assert u.uuid == '1'
    assert u.username == 'u1'
    assert u.email == 'u1@test.com'
    assert u.dni == '12345678A'


def test_create_user_3():
    repo_user = MemoryUsersRepo([User('1', 'u1', 'u1@test.com', '12345678A')])
    c_bus = CommandBus()
    h = CreateUserHandler(repo_user)
    c = CreateUser()
    c_bus.subscribe(CreateUser, h)
    user_info = {
        "uuid": "aaaaa11111",
        "username": "u2",
        "email": "u1@test.com",
        "dni": "12345677A"
    }
    try:
        c_bus.dispatch(c.c_name, user_info)
    except Exception as e:
        assert type(e) == EmailAlreadyExists
    else:
        assert False
    users = repo_user.find_all()
    assert len(users) == 1
    u = users[0]
    assert u.uuid == '1'
    assert u.username == 'u1'
    assert u.email == 'u1@test.com'
    assert u.dni == '12345678A'


def test_create_user_4():
    repo_user = MemoryUsersRepo([User('1', 'u1', 'u1@test.com', '12345678A')])
    c_bus = CommandBus()
    h = CreateUserHandler(repo_user)
    c = CreateUser()
    c_bus.subscribe(CreateUser, h)
    user_info = {
        "uuid": "aaaaa11111",
        "username": "u2",
        "email": "u2@test.com",
        "dni": "12345678A"
    }
    try:
        c_bus.dispatch(c.c_name, user_info)
    except Exception as e:
        assert type(e) == DNIAlreadyExists
    else:
        assert False
    users = repo_user.find_all()
    assert len(users) == 1
    u = users[0]
    assert u.uuid == '1'
    assert u.username == 'u1'
    assert u.email == 'u1@test.com'
    assert u.dni == '12345678A'


def test_create_user_5():
    repo_user = MemoryUsersRepo([User('1', 'u1', 'u1@test.com', '12345678A')])
    c_bus = CommandBus()
    h = CreateUserHandler(repo_user)
    c = CreateUser()
    c_bus.subscribe(CreateUser, h)
    user_info = {
        "uuid": "aaaaa11111",
        "username": "u2",
        "email": "u2@test.com",
        "dni": ""
    }
    try:
        c_bus.dispatch(c.c_name, user_info)
    except Exception as e:
        assert type(e) == InvalidDNI
    else:
        assert False
    users = repo_user.find_all()
    assert len(users) == 1
    u = users[0]
    assert u.uuid == '1'
    assert u.username == 'u1'
    assert u.email == 'u1@test.com'
    assert u.dni == '12345678A'
