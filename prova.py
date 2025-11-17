from infra import MemoryUsersRepo
from domain import User

r = MemoryUsersRepo([])
u=User('1','u1','','')
r.save(u)
u.username='u2'
users = r.find_all()
print(users[0].username)