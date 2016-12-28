from .abstract_entity import AbstractEntity


class Command(AbstractEntity):
    """
    Special class for message which contains command
    """
    def __init__(self, message):
        super(Command, self).__init__(message)
        self.name = Command.parse_name(message)
        self.args = Command.parse_args(message)

    @staticmethod
    def parse_name(message):
        """
        Parses command name from given message
        :param message: Telegram message object
        :return: Name of command
        """
        return message.text[1:].split(' ')[0].split('@')[0]

    @staticmethod
    def parse_args(message):
        """
        Parses command args from given message
        :param message: Telegram message object
        :return: List of command args
        """
        return message.text.split()[1:]
