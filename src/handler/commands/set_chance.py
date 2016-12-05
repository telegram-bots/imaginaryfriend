from .base import Base
from src.config import chance_manager


class SetChance(Base):
    name = 'set_chance'
    chance_manager = chance_manager

    @staticmethod
    def execute(bot, command):
        try:
            chance = int(command.args[0])

            if chance < 1 or chance > 50:
                raise ValueError

            SetChance.chance_manager.set_chance(chat_id=command.chat_id, chance=chance)

            SetChance.reply(bot, command, 'Set chance to: {}'.format(chance))
        except (IndexError, ValueError):
            SetChance.reply(bot, command, 'Usage: /set_chance 1-50.')
