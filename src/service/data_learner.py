from src.config import redis, tokenizer


class DataLearner:
    def __init__(self):
        self.redis = redis
        self.tokenizer = tokenizer

    def learn(self, message):
        pipe = self.redis.instance().pipeline()

        words = self.tokenizer.extract_words(message)
        for trigram in self.tokenizer.split_to_trigrams(words):
            key = self.tokenizer.to_key(message.chat_id, trigram[:-1])
            last_word = trigram[-1]

            pipe.sadd(key, last_word)

        pipe.execute()
