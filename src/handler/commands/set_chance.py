from .base import Base


class SetChance(Base):
    name = 'set_chance'
    chance_manager = None

    @staticmethod
    def execute(bot, command):
        SetChance.reply(bot, command, 'Command currently disabled')
        return

        try:
            chance = int(command.args[0])

            if chance < 1 or chance > 50:
                raise ValueError

            SetChance.chance_manager.set_chance(chat_id=command.chat_id, chance=chance)

            SetChance.reply(bot, command, 'Set chance to: {}'.format(chance))
        except (IndexError, ValueError):
            SetChance.reply(bot, command, 'Usage: /set_chance 1-50.')
