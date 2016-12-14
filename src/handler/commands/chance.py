from .base import Base
from src.config import chance_repository


class Chance(Base):
    name = 'chance'

    @staticmethod
    def execute(bot, command):
        if command.is_private():
            return Chance.reply(bot, command, 'Command disabled for private chats')

        try:
            new_chance = int(command.args[0])

            if new_chance < 1 or new_chance > 50:
                return Chance.reply(bot, command, 'Usage: /chance 1-50.')

            old_chance = chance_repository.set(chat_id=command.chat_id, new_chance=new_chance)

            Chance.reply(bot, command, 'Change chance from {} to {}'.format(old_chance, new_chance))
        except (IndexError, ValueError):
            Chance.reply(bot, command, 'Current chance: {}'
                         .format(chance_repository.get(command.chat_id)))
