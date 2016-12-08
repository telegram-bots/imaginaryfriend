from .base import Base


class Start(Base):
    name = 'start'

    @staticmethod
    def execute(bot, command):
        Start.reply(bot, command, 'Hi! :3')
