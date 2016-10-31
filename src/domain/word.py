from orator.orm import Model
from orator.orm import has_many
from src.domain.chat import Chat


class Word(Model):
    @has_many
    def chats(self):
        return Chat
