from .base import Base
from src.utils import random_element


class Ping(Base):
    name = 'ping'
    answers = [
        'echo',
        'pong',
        'ACK',
        'reply',
        'pingback'
    ]
    
    @staticmethod
    def execute(bot, command):
        Ping.reply(bot, command, random_element(Ping.answers))
