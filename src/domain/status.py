from .abstract_entity import AbstractEntity
from src.utils import deep_get_attr
from src.config import config
from telegram import Message


class Status(AbstractEntity):
    """
    Special class for message which contains info about status change
    """
    def __init__(self, message: Message):
        super(Status, self).__init__(message)
        self.bot_name = config['bot']['name']

    def is_bot_kicked(self) -> bool:
        """
        Returns True if the bot was kicked from group.
        """
        user_name = deep_get_attr(self.message, 'left_chat_member.username')

        return user_name == self.bot_name

    def is_bot_added(self) -> bool:
        """
        Returns True if the bot was added to group.
        """
        user_name = deep_get_attr(self.message, 'new_chat_member.username')

        return user_name == self.bot_name
