from collections import OrderedDict
from src.config import config
from src.entity.word import Word
from src.entity.pair import Pair


class DataLearner:
    def learn(self, message):
        """
        Split message to trigrams and write to DB
        :param message: Message
        """
        self.__write_new_unique_words(message.words)

        words = self.__normalize_words(message.words)
        while any(word for word in words):
            trigram = words[:3]
            first_word_id, second_word_id, *third_word_id = list(map(
                lambda x: None if x is None else Word.where('word', x).first(['id']).id,
                trigram
            ))
            third_word_id = None if len(third_word_id) == 0 else third_word_id[0]

            words.pop(0)

            pair = Pair.where('chat_id', message.chat_id) \
                .where('first_id', first_word_id) \
                .where('second_id', second_word_id) \
                .first()
            if pair is None:
                pair = Pair.create(chat_id=message.chat_id,
                                   first_id=first_word_id,
                                   second_id=second_word_id)

            reply = pair.replies().where('word_id', third_word_id).first()

            if reply is not None:
                reply.count += 1
                reply.save()
            else:
                pair.replies().create(pair_id=pair.id, word_id=third_word_id)

    def __normalize_words(self, src_words):
        words = [None]
        for word in src_words:
            words.append(word)
            if word[-1] in config['grammar']['end_sentence']:
                words.append(None)
        if words[-1] is not None:
            words.append(None)

        return words

    def __write_new_unique_words(self, words):
        # TODO. Слова должны быть уникальные И ТАКЖЕ ОБЯЗАТЕЛЬНО в оригинальном порядке
        existing_words = Word.where_in('word', words).lists('word').all()
        new_words = [word for word in OrderedDict.fromkeys(words).keys() if word not in existing_words]

        for word in new_words:
            Word.create(word=word)
