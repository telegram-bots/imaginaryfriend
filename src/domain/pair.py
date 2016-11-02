import random
from datetime import datetime, timedelta

from orator.orm import Model
from orator.orm import belongs_to
from orator.orm import has_many

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
            if word[-1:] in Pair.end_sentence:
                words.append(None)
        if words[-1:] is not None:
            words.append(None)

        while any(word for word in words):
            trigram = words[:3]
            words.pop(0)
            trigram_word_ids = list(map(lambda x: None if x is None else src.domain.word.Word.where('word', word).first().id, trigram))
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

    @staticmethod
    def __generate_sentence(message, word_ids):
        sentence = ''
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
            second_words = getattr(reply.word, 'id', [])
            if sentence == '':
                sentence = Pair.__capitalize(pair.second.word) + " "
                word_ids.remove(pair.second.id)
            reply_word = getattr(reply.word, 'word', '')
            if reply_word not in sentence and Pair.__capitalize(reply_word) not in sentence:
                sentence += reply_word
        sentence = sentence.strip()
        if sentence[-1:] not in Pair.end_sentence:
            sentence += random.choice(list(Pair.end_sentence))

        return sentence

    @staticmethod
    def __capitalize(string):
        return string[:1].upper() + string[1:]

    @staticmethod
    def __get_pair(chat_id, first_id, second_ids):
        pairs = Pair.with_('replies')\
            .where('chat_id', chat_id)\
            .where('first_id', first_id)\
            .where_in('second_id', second_ids)\
            .where('created_at', '<', (datetime.now() - timedelta(seconds=10 * 60)))\
            .limit(3)\
            .get()\
            .all()

        return random.choice(pairs) if len(pairs) != 0 else None
