class Command:
    def __init__(self, chat, message, config):
        self.chat    = chat
        self.message = message
        self.config  = config
        self.name    = Command.parse_name(message)
        self.args    = Command.parse_args(message)

    @staticmethod
    def parse_name(message):
        return message.text[1:].split(' ')[0].split('@')[0]

    @staticmethod
    def parse_args(message):
        return message.text.split()[1:]
