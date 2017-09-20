from . import RedisRepository
from src.config import config, encoding


class TrigramRepository(RedisRepository):
    def __init__(self):
        RedisRepository.__init__(self, source_name='trigrams:{}:{}')
        self.counter_source = 'trigrams:count:{}'
        self.separator = config['grammar']['sep']
        self.stop_word = config['grammar']['stop_word']

    def store(self, chat_id, trigrams):
        """
        Store all trigrams
        :param chat_id: ID of chat
        :param trigrams: list or generator of trigrams
        """
        counter_pipe = self.redis.instance().pipeline()
        save_pipe = self.redis.instance().pipeline()

        for trigram in trigrams:
            key = self.source_name.format(chat_id, self.separator.join(trigram[:-1]))
            last_word = trigram[-1]

            counter_pipe.exists(key)
            save_pipe.sadd(key, last_word)

        counter_key = self.counter_source.format(chat_id)
        new_pairs_count = sum(map(lambda x: 1 if x == 0 else 0, counter_pipe.execute()))
        save_pipe.incrby(counter_key, new_pairs_count)
        save_pipe.execute()

    def get_random_reply(self, chat_id, key):
        reply = self.redis.instance().srandmember(self.source_name.format(chat_id, key))
        reply = reply.decode(encoding) if reply is not None else None

        if reply == self.stop_word:
            return None

        return reply

    def count(self, chat_id):
        """
        Counts pairs for given chat_it
        :param chat_id: ID of chat
        :return: How many pairs in this chat
        """
        key = self.counter_source.format(chat_id)
        count = self.redis.instance().get(key)

        return self.to_int(count, 0)

    def clear(self, chat_id):
        """
        Remove all trigrams from chat with chat_id
        :param chat_id: ID of chat
        """
        pattern = self.source_name.format(chat_id, '*')
        self.__remove_keys(pattern)

        counter_key = self.counter_source.format(chat_id)
        self.redis.instance().delete(counter_key)

    def find_word(self, chat_id, similar_word, max_results=10):
        """
        Searches for words similar to given word for chat_id
        :param chat_id: ID of chat
        :param similar_word: Word similar to which we should find
        :param max_results: Max size of list returned
        :return: Unique found words
        """
        format_pattern = self.source_name.format(chat_id, '')
        search_pattern = self.source_name.format(chat_id, '*' + similar_word + '*')
        redis = self.redis.instance()
        words = set()

        for pair in redis.scan_iter(match=search_pattern, count=max_results):
            (first, second) = pair.decode(encoding).lstrip(format_pattern).split(self.separator)
            if first.startswith(similar_word):
                words.add(first)
            if second.startswith(similar_word):
                words.add(second)

        return list(words)[:10]

    def remove_word(self, chat_id, exact_word):
        """
        Removes words with exact match to given word for chat_id
        :param chat_id: ID of chat
        :param exact_word: Exact word match
        """
        self.__remove_keys(self.source_name.format(chat_id, exact_word + "\\" + self.separator + '*'))
        self.__remove_keys(self.source_name.format(chat_id, '*' + "\\" + self.separator + exact_word))

    # FIXME. Not optimal performance wise
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
