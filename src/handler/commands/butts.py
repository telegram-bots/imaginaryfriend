from .base import Base
import json
from src.component.config import encoding
from urllib.request import urlopen


class Butts(Base):
    name = 'butts'
    aliases = ['(_._)', '(_*_)', '(Y)']

    def execute(self, command):
        response = urlopen('http://api.obutts.ru/noise/1')
        data = json.loads(response.read().decode(encoding))
        url = 'http://media.obutts.ru/' + data[0]['preview']

        self.send_photo(command, photo=url)
