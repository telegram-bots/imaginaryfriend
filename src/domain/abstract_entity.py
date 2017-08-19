from abc import ABC


class AbstractEntity(ABC):
    """
    Base class for all message entities
    """

    def __init__(self, message):
        self.chat_id = message.chat.id
        self.chat_type = message.chat.type
        self.message = message

    def is_private(self):
        """Returns True if chat type is private.
        """
        return self.message.chat.type == 'private'

    def is_editing(self):
        """Returns True if the message was edited.
        """
        return self.message.edit_date is not None

    def __str__(self):
        return str(self.__dict__)
