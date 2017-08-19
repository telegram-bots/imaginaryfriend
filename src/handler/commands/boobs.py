from .base import Base
import json
from urllib.request import urlopen
from src.config import encoding


class Boobs(Base):
    name = 'boobs'
    aliases = ['80085', '(.)(.)']

    def execute(self, command):
        response = urlopen('http://api.oboobs.ru/noise/1')
        data = json.loads(response.read().decode(encoding))
        url = 'http://media.oboobs.ru/' + data[0]['preview']

        self.send_photo(command, photo=url)
