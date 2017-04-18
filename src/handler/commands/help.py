from .base import Base
from src.utils import read_to_string


class Help(Base):
    name = 'help'
    text = read_to_string('info/help.txt')

    @staticmethod
    def execute(bot, command):
        Help.reply(bot, command, Help.text)
