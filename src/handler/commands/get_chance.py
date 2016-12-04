from .base import Base


class GetChance(Base):
    name = 'get_chance'
    chance_manager = None

    @staticmethod
    def execute(bot, command):
        GetChance.reply(bot, command, 'Command currently disabled')
        return

        GetChance.reply(bot, command, 'Current chance: {}'
                        .format(GetChance.chance_manager.get_chance(command.chat_id)))
