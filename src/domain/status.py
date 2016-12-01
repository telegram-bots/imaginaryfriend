from .abstract_entity import AbstractEntity
from src.utils import deep_get_attr
from src.config import config


class Status(AbstractEntity):
    def __init__(self, message):
        super(Status, self).__init__(message)

    def is_bot_kicked(self):
        """Returns True if the bot was kicked from group.
        """
        user_name = deep_get_attr(self.message, 'left_chat_member.username')

        return user_name == config['bot']['name']

    def is_bot_added(self):
        """Returns True if the bot was added to group.
        """
        user_name = deep_get_attr(self.message, 'new_chat_member.username')

        return user_name == config['bot']['name']
