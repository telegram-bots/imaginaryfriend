from orator.orm import Model
from orator.orm import has_many

import src.domain.chat


class Word(Model):
    __guarded__ = ['id']
    __timestamps__ = False

    @has_many
    def chats(self):
        return src.domain.chat.Chat

    @staticmethod
    def learn(words):
        existing_words = Word.where_in('word', words).get().pluck('word').all()
        
        new_words = {word for word in words}.difference(existing_words)

        if len(new_words):
            for word in new_words:
                Word.create(word=word)
