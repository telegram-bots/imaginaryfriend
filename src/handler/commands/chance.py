from .base import Base
from src.config import chance_manager


class Chance(Base):
    name = 'chance'
    chance_manager = chance_manager

    @staticmethod
    def execute(bot, command):
        try:
            new_chance = int(command.args[0])

            if new_chance < 1 or new_chance > 50:
                return Chance.reply(bot, command, 'Usage: /chance 1-50.')

            old_chance = Chance.chance_manager.set_chance(chat_id=command.chat_id, new_chance=new_chance)

            Chance.reply(bot, command, 'Change chance from {} to {}'.format(old_chance, new_chance))
        except (IndexError, ValueError):
            Chance.reply(bot, command, 'Current chance: {}'
                         .format(Chance.chance_manager.get_chance(command.chat_id)))
