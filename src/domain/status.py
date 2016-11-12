from src.utils import deep_get_attr


class Status:
    def __init__(self, chat, message, config):
        self.chat    = chat
        self.message = message
        self.config  = config

    def is_bot_kicked(self):
        """Returns True if the bot was kicked from group.
        """
        user_name = deep_get_attr(self.message, 'left_chat_member.username')

        return user_name == self.config['bot']['name']

    def is_bot_added(self):
        """Returns True if the bot was added to group.
        """
        user_name = deep_get_attr(self.message, 'new_chat_member.username')

        return user_name == self.config['bot']['name']
