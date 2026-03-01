class QueryBus:
    def __init__(self,):
        self.handlers = {}

    def subscribe(self, query_class, handler):
        self.handlers[query_class.q_name] = handler

    def dispatch(self, q_name):
        return self.handlers[q_name].execute()


class CommandBus:
    def __init__(self,):
        self.handlers = {}

    def subscribe(self, command_class, handler):
        self.handlers[command_class.c_name] = handler

    def dispatch(self, c_name,c_info):
        return self.handlers[c_name].execute(c_info)

def init_buses(cmd_bus,q_bus):
    from hex.users.infra import DjangoUsersRepo
    from hex.users.domain import User
    from hex.users.app import CreateUser, CreateUserHandler
    from hex.users.app import GetUsers, GetUsersHandler
    from hex.users.domain import User

    # u = User('1', 'u1', 'u1@test.com', '12345678A')
    # repo_user = MemoryUsersRepo([u])
    repo_user = DjangoUsersRepo()
    command_h = CreateUserHandler(repo_user)
    cmd_bus.subscribe(CreateUser, command_h)

    h = GetUsersHandler(repo_user)
    q_bus.subscribe(GetUsers, h)

q_bus = QueryBus()
c_bus = CommandBus()