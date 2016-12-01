from abc import ABC


class AbstractEntity(ABC):
    def __init__(self, message):
        self.chat_id = message.chat.id
        self.chat_type = message.chat.type
        self.message = message
