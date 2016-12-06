from src.config import config, redis


class ChanceManager:
    def __init__(self):
        self.redis = redis
        self.key = "chance:{}"
        self.default_chance = config.getint('bot', 'default_chance')

    def get_chance(self, chat_id):
        result = self.redis.instance().get(self.key.format(chat_id))

        return int(result.decode("utf-8")) if result is not None else self.default_chance

    def set_chance(self, chat_id, chance):
        self.redis.instance().set(self.key.format(chat_id), chance)
