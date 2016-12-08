from src.config import config, redis


class ChanceManager:
    def __init__(self):
        self.redis = redis
        self.key = 'chance:{}'
        self.default_chance = config.getint('bot', 'default_chance')

    def get_chance(self, chat_id):
        result = self.redis.instance().get(self.key.format(chat_id))

        return int(result.decode("utf-8")) if result is not None else self.default_chance

    def set_chance(self, chat_id, new_chance):
        old_chance = self.redis.instance().getset(self.key.format(chat_id), new_chance)

        return int(old_chance.decode("utf-8")) if old_chance is not None else self.default_chance
