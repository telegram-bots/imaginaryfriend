from orator.orm import Model
from orator.orm import belongs_to
from orator.orm import has_many

import src.domain.reply
import src.domain.chat
import src.domain.word


class Pair(Model):
    __guarded__ = ['id']

    # TODO Move to config
    end_sentence = '.!?'
    all = '.!?,;:'

    @has_many
    def replies(self):
        return src.domain.reply.Reply

    @belongs_to
    def chat(self):
        return src.domain.chat.Chat

    @staticmethod
    def generate(message):
        return ''
    #     generate_story(message, message.words, rand(2) + 1)

    @staticmethod
    def learn(message):
        src.domain.word.Word.learn(message.words)

        print("Msg words: " + str(message.words))

        words = [None]
        for word in message.words:
            words.append(word)
            if word[-1:] in Pair.end_sentence:
                words.append(None)
        if words[-1:] is not None:
            words.append(None)

        print("Words: "+str(words))

        while any(word for word in words):
            trigram = words[:3]
            words.pop(0)
            print("Trigram: " + str(trigram))
            trigram_word_ids = list(map(lambda x: None if x is None else src.domain.word.Word.where('word', word).first().id, trigram))
            print("TrigramId: " + str(trigram_word_ids))
            pair = Pair.first_or_create(chat_id=message.chat.id,
                                        first_id=trigram_word_ids[0],
                                        second_id=trigram_word_ids[1])
            last_trigram_id = trigram_word_ids[2] if len(trigram_word_ids) == 3 else None
            reply = pair.replies().where('word_id', last_trigram_id).first()

            if reply is not None:
                reply.count += 1
                reply.save()
            else:
                src.domain.reply.Reply.create(pair_id=pair.id, word_id=last_trigram_id)


    # @staticmethod
    # def get_pair(chat_id, first_id, second_id):
    #     Pair.includes(Pair.replies())
    #     .where(chat_id: chat_id, first_id: first_id, second_id: second_id)
    #     .where("created_at < :latest", latest: 10.minutes.ago)
    #     .limit(3)\
    #     .sample