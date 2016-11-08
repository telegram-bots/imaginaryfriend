from datetime import datetime, timedelta

from orator.orm import Model
from orator.orm import belongs_to
from orator.orm import has_many

from src.utils import *

import src.domain.chat
import src.domain.reply
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

    @belongs_to
    def first(self):
        return src.domain.word.Word

    @belongs_to
    def second(self):
        return src.domain.word.Word

    @staticmethod
    def generate(message):
        return Pair.generate_story(message, message.words, random.randint(0, 2) + 1)

    @staticmethod
    def generate_story(message, words, sentences):
        words_ids = src.domain.word.Word.where_in('word', words).get().pluck('id').all()

        result = []
        for _ in range(0, sentences):
            result.append(Pair.__generate_sentence(message, words_ids))

        return ' '.join(result)

    @staticmethod
    def learn(message):
        src.domain.word.Word.learn(message.words)

        words = [None]
        for word in message.words:
            words.append(word)
            if word[-1] in Pair.end_sentence:
                words.append(None)
        if words[-1] is not None:
            words.append(None)

        while any(word for word in words):
            trigram = words[:3]
            words.pop(0)
            trigram_word_ids = list(map(
                lambda x: None if x is None else src.domain.word.Word.where('word', x).first().id,
                trigram
            ))

            pair = Pair.where('chat_id', message.chat.id)\
                .where('first_id', trigram_word_ids[0])\
                .where('second_id', trigram_word_ids[1])\
                .first()
            if pair is None:
                pair = Pair.create(chat_id=message.chat.id,
                                   first_id=trigram_word_ids[0],
                                   second_id=trigram_word_ids[1])

            last_trigram_id = trigram_word_ids[2] if len(trigram_word_ids) == 3 else None
            reply = pair.replies().where('word_id', last_trigram_id).first()

            if reply is not None:
                reply.count += 1
                reply.save()
            else:
                src.domain.reply.Reply.create(pair_id=pair.id, word_id=last_trigram_id)

    @staticmethod
    def __generate_sentence(message, word_ids):
        sentences = []
        safety_counter = 50
        first_word = None
        second_words = list(word_ids)

        while safety_counter > 0:
            pair = Pair.__get_pair(chat_id=message.chat.id, first_id=first_word, second_ids=second_words)
            replies = getattr(pair, 'replies', [])
            safety_counter -= 1

            if pair is None or len(replies) == 0:
                continue

            reply = random.choice(replies.all())
            first_word = pair.second.id

            # TODO. WARNING! Do not try to fix, it's magic, i have no clue why
            try:
                second_words = [reply.word.id]
            except AttributeError:
                second_words = None

            if len(sentences) == 0:
                sentences.append(capitalize(pair.second.word) + " ")
                word_ids.remove(pair.second.id)

            # TODO. WARNING! Do not try to fix, it's magic, i have no clue why
            try:
                reply_word = reply.word.word
            except AttributeError:
                reply_word = None

            if reply_word is not None:
                sentences.append(reply_word)
            else:
                break

        sentence = ' '.join(sentences).strip()
        if sentence[-1:] not in Pair.end_sentence:
            sentence += random.choice(list(Pair.end_sentence))

        return sentence

    @staticmethod
    def __get_pair(chat_id, first_id, second_ids):
        ten_minutes_ago = datetime.now() - timedelta(seconds=10 * 60)
        pairs = Pair.with_('replies')\
            .where('chat_id', chat_id)\
            .where('first_id', first_id)\
            .where_in('second_id', second_ids)\
            .where('created_at', '<', ten_minutes_ago)\
            .limit(3)\
            .get()\
            .all()

        return random_element(pairs)
