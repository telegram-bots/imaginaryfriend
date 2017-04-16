from .base import Base
import json
from urllib.request import urlopen


class Boobs(Base):
    name = 'boobs'
    aliases = ['80085', '(.)(.)']

    @staticmethod
    def execute(bot, command):
        response = urlopen('http://api.oboobs.ru/noise/1')
        data = json.loads(response.read().decode('utf-8'))
        url = 'http://media.oboobs.ru/' + data[0]['preview']

        bot.send_photo(chat_id=command.chat_id, photo=url)
