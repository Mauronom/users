class QueryBus:
    def __init__(self,):
        self.handlers = {}

    def subscribe(self, query_class, handler):
        self.handlers[query_class.q_name] = handler

    def dispatch(self, q):
        return self.handlers[q.q_name].execute()