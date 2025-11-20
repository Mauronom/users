from infra import MemoryUsersRepo
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
