from .base import Base
from urllib.request import build_opener, HTTPRedirectHandler


class Meow(Base):
    name = 'meow'
    aliases = [':3', '=3']

    @staticmethod
    def execute(bot, command):
        opener = build_opener(HTTPRedirectHandler)
        request = opener.open('http://thecatapi.com/api/images/get?format=src')
        url = request.url

        bot.send_photo(chat_id=command.chat_id, photo=url)
