class QueryBus:
    def __init__(self):
        self.handlers = {}
        self.classes = {}

    def get_query_class(self, q_name):
        return self.classes[q_name]

    def subscribe(self, query_class, handler):
        self.classes[query_class.q_name] = query_class
        self.handlers[query_class.q_name] = handler

    def dispatch(self, q):
        return self.handlers[q.q_name].execute(q)


class CommandBus:
    def __init__(self):
        self.handlers = {}
        self.classes = {}

    def get_command_class(self, c_name):
        return self.classes[c_name]

    def subscribe(self, command_class, handler):
        self.classes[command_class.c_name] = command_class
        self.handlers[command_class.c_name] = handler

    def dispatch(self, cmd):
        return self.handlers[cmd.c_name].execute(cmd)


def init_buses(cmd_bus, q_bus):
    from django.conf import settings
    from hex.mailing.infra.repos import DjangoContactsRepo, DjangoTemplatesRepo, DjangoMailsRepo
    from hex.mailing.infra.gmail_sender import GmailSender
    from hex.mailing.app import CreateMail, CreateMailHandler, SendMail, SendMailHandler

    handler = CreateMailHandler(DjangoTemplatesRepo(), DjangoContactsRepo(), DjangoMailsRepo())
    cmd_bus.subscribe(CreateMail, handler)

    sender = GmailSender(settings.GMAIL_CREDENTIALS_PATH, settings.GMAIL_TOKEN_PATH)
    send_handler = SendMailHandler(DjangoMailsRepo(), sender)
    cmd_bus.subscribe(SendMail, send_handler)


q_bus = QueryBus()
c_bus = CommandBus()
