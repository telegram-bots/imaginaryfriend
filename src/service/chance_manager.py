from src.config import config, redis


class ChanceManager:
    """
    Handles bot reply chance
    """
    def __init__(self):
        self.redis = redis
        self.key = 'chance:{}'
        self.default_chance = config.getint('bot', 'default_chance')

    def get_chance(self, chat_id):
        """
        Returns current chance of bot reply for chat_id
        :param chat_id: ID of chat
        :return: Current chance
        """
        result = self.redis.instance().get(self.key.format(chat_id))

        return int(result.decode("utf-8")) if result is not None else self.default_chance

    def set_chance(self, chat_id, new_chance):
        """
        Sets new reply chance for chat_id and returns old
        :param chat_id: ID of chat
        :param new_chance: Chance to set
        :return: Old chance
        """
        old_chance = self.redis.instance().getset(self.key.format(chat_id), new_chance)

        return int(old_chance.decode("utf-8")) if old_chance is not None else self.default_chance
