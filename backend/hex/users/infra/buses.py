class QueryBus:
    def __init__(self,):
        self.handlers = {}

    def subscribe(self, query_class, handler):
        self.handlers[query_class.q_name] = handler

    def dispatch(self, q):
        return self.handlers[q.q_name].execute(q)


class CommandBus:
    def __init__(self,):
        self.handlers = {}

    def subscribe(self, command_class, handler):
        self.handlers[command_class.c_name] = handler

    def dispatch(self, cmd):
        return self.handlers[cmd.c_name].execute(cmd)

def init_buses(cmd_bus,q_bus):
    from hex.users.infra import DjangoUsersRepo
    from hex.users.app import CreateUser, CreateUserHandler
    from hex.users.app import GetUsers, GetUsersHandler

    repo_user = DjangoUsersRepo()
    command_h = CreateUserHandler(repo_user)
    cmd_bus.subscribe(CreateUser, command_h)

    h = GetUsersHandler(repo_user)
    q_bus.subscribe(GetUsers, h)

q_bus = QueryBus()
c_bus = CommandBus()
