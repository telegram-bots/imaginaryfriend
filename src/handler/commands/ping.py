from .base import Base
from random import choice


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
        self.reply(command, choice(self.answers))
