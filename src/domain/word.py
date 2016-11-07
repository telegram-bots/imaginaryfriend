from orator.orm import Model
from orator.orm import has_many

import src.domain.chat
from collections import OrderedDict


class Word(Model):
    __guarded__ = ['id']
    __timestamps__ = False

    @has_many
    def chats(self):
        return src.domain.chat.Chat

    @staticmethod
    def learn(words):
        existing_words = Word.where_in('word', words).get().pluck('word').all()
        # TODO. Слова должны быть уникальные И ТАКЖЕ ОБЯЗАТЕЛЬНО в оригинальном порядке
        new_words = [word for word in OrderedDict.fromkeys(words).keys() if word not in existing_words]

        for word in new_words:
            Word.create(word=word)
