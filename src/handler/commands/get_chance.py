from .base import Base
from src.config import chance_manager


class GetChance(Base):
    name = 'get_chance'
    chance_manager = chance_manager

    @staticmethod
    def execute(bot, command):
        GetChance.reply(bot, command, 'Current chance: {}'
                        .format(GetChance.chance_manager.get_chance(command.chat_id)))
