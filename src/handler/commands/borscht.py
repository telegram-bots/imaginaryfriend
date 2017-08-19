from .base import Base
import json
from src.utils import random_element
from src.config import encoding
from urllib.request import urlopen


class Borscht(Base):
    name = 'borscht'
    images = None

    def __init__(self):
        super().__init__()
        self.images = self.__preload()

    def execute(self, command):
        self.send_photo(command, photo=random_element(Borscht.images))

    def __preload(self):
        response = urlopen('https://api.cognitive.microsoft.com/bing/v5.0/images/search?q=%D0%B1%D0%BE%D1%80%D1%89&mkt=en-us&safe-search=strict&image-type=photo&subscription-key=dd95294bc02748a1ab5152d36fdbbdac')
        data = json.loads(response.read().decode(encoding))

        return list(map(lambda e: e['contentUrl'], data['value']))
