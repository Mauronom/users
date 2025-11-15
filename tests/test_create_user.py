from infra import MemoryUsersRepo
from app import CreateUser

def test_create_user_1():
    repo_user = MemoryUsersRepo([])
    cmd = CreateUser(repo_user)
    cmd.execute('aaaaa11111','username1','email@test.com','12345678A')
    users = repo_user.find_all()
    assert len(users)==1
    u = users[0]
    assert u.uuid=='aaaaa11111'
    assert u.username=='username1'
    assert u.email=='email@test.com'
    assert u.dni=='12345678A'