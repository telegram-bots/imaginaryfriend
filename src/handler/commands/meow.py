from .base import Base
from urllib.request import build_opener, HTTPRedirectHandler


class Meow(Base):
    name = 'meow'
    aliases = [':3', '=3']

    def execute(self, command):
        opener = build_opener(HTTPRedirectHandler)
        req = opener.open('http://thecatapi.com/api/images/get?format=src')

        self.send_photo(command, photo=req.url)
