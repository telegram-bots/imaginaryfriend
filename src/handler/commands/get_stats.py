from .base import Base
from src.config import trigram_repository


class GetStats(Base):
    name = 'get_stats'

    def execute(self, command):
        pairs_count = trigram_repository.count(command.chat_id)
        self.reply(command, 'Pairs: {}'.format(pairs_count))
