import random
from .abstract_entity import AbstractEntity
from telegram import Message as TMessage
from src.utils import deep_get_attr
from src.config import config


class Message(AbstractEntity):
    """
    Basic message entity
    """
    def __init__(self, chance: int, message: TMessage):
        super(Message, self).__init__(message)

        self.chance = chance
        self.entities = message.entities
        self.anchors = config.getlist('bot', 'anchors')

        if self.has_text():
            self.text = message.text
        else:
            self.text = ''

    def has_text(self) -> bool:
        """
        Returns True if the message has text.
        """
        return self.message.text.strip() != ''

    def is_sticker(self) -> bool:
        """
        Returns True if the message is a sticker.
        """
        return self.message.sticker is not None

    def has_entities(self) -> bool:
        """
        Returns True if the message has entities (attachments).
        """
        return self.entities is not None

    def has_anchors(self) -> bool:
        """
        Returns True if the message contains at least one anchor from anchors config.
        """
        return self.has_text() and any(a in self.message.text.split(' ') for a in self.anchors)

    def is_reply_to_bot(self) -> bool:
        """
        Returns True if the message is a reply to bot.
        """
        user_name = deep_get_attr(self.message, 'reply_to_message.from_user.username')

        return user_name == config['bot']['name']

    def is_random_answer(self) -> bool:
        """
        Returns True if reply chance for this chat is high enough
        """
        return random.randint(0, 100) < self.chance

    def should_answer(self) -> bool:
        """
        Returns True if bot should answer to this message
        :return: Should answer or not
        """
        return self.has_anchors() \
            or self.is_private() \
            or self.is_reply_to_bot() \
            or self.is_random_answer()
