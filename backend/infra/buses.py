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

