from orator.orm import Model
from orator.orm import has_many

import src.entity.chat


class Word(Model):
    __fillable__ = ['word']
    __timestamps__ = False

    @has_many
    def chats(self):
        return src.entity.chat.Chat
