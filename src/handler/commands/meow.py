from .base import Base
from urllib.request import build_opener, HTTPRedirectHandler
import json


class Meow(Base):
    name = 'meow'
    aliases = [':3', '=3']

    def execute(self, command):
        opener = build_opener(HTTPRedirectHandler)
        with opener.open('https://api.thecatapi.com/v1/images/search') as r:
            cats = json.loads(r.read())

        self.send_photo(command, photo=cats[0]['url'])
