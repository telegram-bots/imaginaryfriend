from .base import Base
import json
import random
from urllib.request import urlopen


class XKCD(Base):
    name = 'xkcd'

    @staticmethod
    def execute(bot, command):
        last_id = json.loads(urlopen("http://xkcd.com/info.0.json").read().decode('utf-8'))['num']
        id = random.randint(1, last_id)
        url = json.loads(urlopen('http://xkcd.com/' + str(id) + '/info.0.json').read().decode('utf-8'))['img']

        bot.send_photo(chat_id=command.chat_id, photo=url)
