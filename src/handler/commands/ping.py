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

    def execute(self, command):
        self.reply(command, random_element(Ping.answers))
