from .base import Base


class GetStats(Base):
    name = 'get_stats'

    @staticmethod
    def execute(bot, command):
        GetStats.reply(bot, command, 'Command currently disabled')
        # GetStats.reply(bot, command, 'Pairs: {}'.format(Pair.where('chat_id', command.chat_id).count()))
