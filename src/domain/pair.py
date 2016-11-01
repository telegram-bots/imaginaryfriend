from orator.orm import Model
from orator.orm import belongs_to
from orator.orm import has_many

from . import (Reply, Chat, Word)


class Pair(Model):
    __guarded__ = ['id']

    # TODO Move to config
    end_sentence = '.!?'
    all = '.!?,;:'

    @has_many
    def replies(self):
        return Reply

    @belongs_to
    def chat(self):
        return Chat

    @staticmethod
    def generate(message):
        return ''
    #     generate_story(message, message.words, rand(2) + 1)

    @staticmethod
    def learn(message):
        Word.learn(message.words)

        words = [None]
        for word in message.words:
            words.append(word)
            if word[-1:] in Pair.end_sentence:
                words.append(None)
        if words[-1:] is not None:
            words.append(None)

        while any(word for word in words):
            trigram = words[:3]
            words.pop(0)
            trigram_word_ids = list(map(lambda x: None if x is None else Word.where('word', word).first().id, trigram))

            pair = Pair.first_or_create(chat_id=message.chat.id,
                                        first_id=trigram_word_ids[0],
                                        second_id=trigram_word_ids[1])
            reply = pair.replies().where('word_id', trigram_word_ids[2]).first()

            if reply is not None:
                reply.increment('count')
            else:
                Reply.create(pair_id=pair.id, word_id=trigram_word_ids[2])


    # @staticmethod
    # def get_pair(chat_id, first_id, second_id):
    #     Pair.includes(Pair.replies())
    #     .where(chat_id: chat_id, first_id: first_id, second_id: second_id)
    #     .where("created_at < :latest", latest: 10.minutes.ago)
    #     .limit(3)\
    #     .sample