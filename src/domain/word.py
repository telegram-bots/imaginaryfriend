from orator.orm import Model
from orator.orm import has_many
from . import Chat


class Word(Model):
    __guarded__ = ['id']

    @has_many
    def chats(self):
        return Chat

    @staticmethod
    def learn(words):
        existing_words = Word.where_in('word', words).get().pluck('word').all()
        new_words = list(set([word for word in words if word not in existing_words]))
        if len(new_words):
            Word.insert(zip(['word'] * len(new_words), new_words))
