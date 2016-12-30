from .abstract_entity import AbstractEntity
from telegram import Message
from typing import List


class Command(AbstractEntity):
    """
    Special class for message which contains command
    """
    def __init__(self, message: Message):
        super(Command, self).__init__(message)
        self.name = Command.parse_name(message)
        self.args = Command.parse_args(message)

    @staticmethod
    def parse_name(message: Message) -> str:
        """
        Parses command name from given message
        :param message: Telegram message object
        :return: Name of command
        """
        return message.text[1:].split(' ')[0].split('@')[0]

    @staticmethod
    def parse_args(message: Message) -> List[str]:
        """
        Parses command args from given message
        :param message: Telegram message object
        :return: List of command args
        """
        return message.text.split()[1:]
