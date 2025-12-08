from infra import MemoryUsersRepo, CommandBus
from app import CreateUserHandler, CreateUser
from domain import User

r = MemoryUsersRepo([])
u = User('1', 'u1', '', '')
r.save(u)
u.username = 'u2'
users = r.find_all()
print(users[0].username)



u = User("1", 'u2', 'asdfsd', '')
r.save(u)
users = r.find_by_field("uuid", "1")
for user in users:
    print("user:",user.username)
    print("mail:",user.email)



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
users = c_bus.dispatch(c.c_name, user_info)

