from .base import Base
from src.config import trigram_repository


class GetStats(Base):
    name = 'get_stats'

    @staticmethod
    def execute(bot, command):
        pairs_count = trigram_repository.count(command.chat_id)
        GetStats.reply(bot, command, 'Pairs: {}'.format(pairs_count))
