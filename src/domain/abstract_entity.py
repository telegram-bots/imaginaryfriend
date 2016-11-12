from abc import ABC


class AbstractEntity(ABC):
    def __init__(self, chat, message):
        self.chat = chat
        self.message = message
