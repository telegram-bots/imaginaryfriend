from .base import Base
import json
from urllib.request import urlopen


class Butts(Base):
    name = 'butts'
    aliases = ['(_._)', '(_*_)', '(Y)']

    @staticmethod
    def execute(bot, command):
        response = urlopen('http://api.obutts.ru/noise/1')
        data = json.loads(response.read().decode('utf-8'))
        url = 'http://media.obutts.ru/' + data[0]['preview']

        bot.send_photo(chat_id=command.chat_id, photo=url)
