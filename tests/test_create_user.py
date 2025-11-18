from infra import MemoryUsersRepo
from app import CreateUser
from domain import User


def test_create_user_1():
    repo_user = MemoryUsersRepo([])
    cmd = CreateUser(repo_user)
    cmd.execute('aaaaa11111', 'username1', 'email@test.com', '12345678A')
    users = repo_user.find_all()
    assert len(users) == 1
    u = users[0]
    assert u.uuid == 'aaaaa11111'
    assert u.username == 'username1'
    assert u.email == 'email@test.com'
    assert u.dni == '12345678A'


def test_create_user_2():
    repo_user = MemoryUsersRepo([User('1','u1','u1@test.com','12345678A')])
    cmd = CreateUser(repo_user)
    try:
        cmd.execute('aaaaa11111', 'u1', 'email@test.com', '12345677A')
    except Exception as e:
        assert type(e) == UsernameAlreadyExists
    else:
        assert False
    users = repo_user.find_all()
    assert len(users) == 1
    u = users[0]
    assert u.uuid == '1'
    assert u.username == 'u1'
    assert u.email == 'email@test.com'
    assert u.dni == '12345678A'

def test_create_user_3():
    repo_user = MemoryUsersRepo([User('1','u1','u1@test.com','12345678A')])
    cmd = CreateUser(repo_user)
    try:
        cmd.execute('aaaaa11111', 'u2', 'u1@test.com', '12345677A')
    except Exception as e:
        assert type(e) == EmailAlreadyExists
    else:
        assert False
    users = repo_user.find_all()
    assert len(users) == 1
    u = users[0]
    assert u.uuid == '1'
    assert u.username == 'u1'
    assert u.email == 'email@test.com'
    assert u.dni == '12345678A'

def test_create_user_4():
    repo_user = MemoryUsersRepo([User('1','u1','u1@test.com','12345678A')])
    cmd = CreateUser(repo_user)
    try:
        cmd.execute('aaaaa11111', 'u2', 'u2@test.com', '12345678A')
    except Exception as e:
        assert type(e) == DNIAlreadyExists
    else:
        assert False
    users = repo_user.find_all()
    assert len(users) == 1
    u = users[0]
    assert u.uuid == '1'
    assert u.username == 'u1'
    assert u.email == 'email@test.com'
    assert u.dni == '12345678A'


def test_create_user_5():
    repo_user = MemoryUsersRepo([User('1','u1','u1@test.com','12345678A')])
    cmd = CreateUser(repo_user)
    try:
        cmd.execute('aaaaa11111', 'u2', 'u2@test.com', '')
    except Exception as e:
        assert type(e) == InvalidDNI
    else:
        assert False
    users = repo_user.find_all()
    assert len(users) == 1
    u = users[0]
    assert u.uuid == '1'
    assert u.username == 'u1'
    assert u.email == 'email@test.com'
    assert u.dni == '12345678A'
