from . import RedisRepository
from src.config import config, encoding


class TrigramRepository(RedisRepository):
    def __init__(self):
        RedisRepository.__init__(self, source_name='trigrams:{}:{}')
        self.separator = config['grammar']['separator']

    def store(self, chat_id, trigrams):
        """
        Store all trigrams
        :param chat_id: ID of chat
        :param trigrams: list or generator of trigrams
        """
        pipe = self.redis.instance().pipeline()

        for trigram in trigrams:
            key = self.source(chat_id, self.separator.join(trigram[:-1]))
            last_word = trigram[-1]

            pipe.sadd(key, last_word)

        pipe.execute()

    def count(self, chat_id):
        """
        Counts pairs for given chat_it
        :param chat_id: ID of chat
        :return: How many pairs in this chat
        """
        pattern = self.source(chat_id, '*')
        redis = self.redis.instance()

        counter = 0
        for _ in redis.scan_iter(match=pattern, count=10000):
            counter += 1

        return counter

    def clear(self, chat_id):
        """
        Remove all trigrams from chat with chat_id
        :param chat_id: ID of chat
        """
        pattern = self.source(chat_id, '*')
        self.__remove_by_pattern(pattern)

    def find_word(self, chat_id, similar_word):
        """
        Searches for words similar to given word for chat_id
        :param chat_id: ID of chat
        :param similar_word: Word similar to which we should find
        :return: Unique found words
        """
        format_pattern = self.source(chat_id, '')
        search_pattern = self.source(chat_id, '*' + similar_word + '*')
        redis = self.redis.instance()
        words = set()

        for pair in redis.scan_iter(match=search_pattern, count=10000):
            (first, second) = pair.decode(encoding).lstrip(format_pattern).split(self.separator)
            words.add(first if similar_word in first else second)

        return words

    def remove_word(self, chat_id, exact_word):
        """
        Removes words with exact match to given word for chat_id
        :param chat_id: ID of chat
        :param exact_word: Exact word match
        """

        self.__remove_by_pattern(self.source(chat_id, exact_word + self.separator + '*'))
        self.__remove_by_pattern(self.source(chat_id, '*' + self.separator + exact_word))

    def __remove_keys(self, pattern):
        """
        Remove all keys matching given pattern
        :param pattern: Pattern to match
        """
        redis = self.redis.instance()
        pipe = redis.pipeline()

        for key in redis.scan_iter(match=pattern, count=10000):
            pipe.delete(key.decode(encoding))

        pipe.execute()
