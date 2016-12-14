from . import RedisRepository
from src.config import config


class TrigramRepository(RedisRepository):
    def __init__(self):
        RedisRepository.__init__(self, source_name='trigrams:{}:{}')
        self.separator = config['grammar']['separator']

    def store(self, chat_id, trigrams):
        pipe = self.redis.instance().pipeline()

        for trigram in trigrams:
            key = self.source(chat_id, trigram[:-1])
            last_word = trigram[-1]

            pipe.sadd(key, last_word)

        pipe.execute()

    def count(self, chat_id):
        """
        Counts pairs for given chat_it
        :param chat_id: ID of chat
        :return: How many pairs in this chat
        """
        pattern = self.source_name.format(chat_id, '*')
        redis = self.redis.instance()

        counter = 0
        for _ in redis.scan_iter(match=pattern, count=10000):
            counter += 1

        return counter

    def source(self, chat_id, pair):
        """
        Overridden source method, to accept pair
        :param chat_id: ID of chat
        :param pair: Pair
        :return: Source name
        """
        return self.source_name.format(chat_id, self.separator.join(pair))
