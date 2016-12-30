from abc import ABC
from telegram import Message


class AbstractEntity(ABC):
    """
    Base class for all message entities
    """

    def __init__(self, message: Message):
        self.chat_id = message.chat.id
        self.chat_type = message.chat.type
        self.message = message

    def is_private(self) -> bool:
        """Returns True if chat type is private.
        """
        return self.message.chat.type == 'private'

    def is_editing(self) -> bool:
        """Returns True if the message was edited.
        """
        return self.message.edit_date is not None
