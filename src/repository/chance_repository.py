from . import RedisRepository
from src.config import config


class ChanceRepository(RedisRepository):
    def __init__(self):
        RedisRepository.__init__(self, source_name='chance:{}')
        self.default_chance = config.getint('bot', 'default_chance')

    def get(self, chat_id: int) -> int:
        """
        Returns current chance of bot reply for chat_id
        :param chat_id: ID of chat
        :return: Current chance
        """
        key = self.source_name.format(chat_id)
        chance = self.redis.instance().get(key)

        return self.to_int(chance, self.default_chance)

    def set(self, chat_id: int, new_chance: int) -> int:
        """
        Sets new reply chance for chat_id and returns old
        :param chat_id: ID of chat
        :param new_chance: Chance to set
        :return: Old chance
        """
        key = self.source_name.format(chat_id)
        old_chance = self.redis.instance().getset(key, new_chance)

        return self.to_int(old_chance, self.default_chance)

