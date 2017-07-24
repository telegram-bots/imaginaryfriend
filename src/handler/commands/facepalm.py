from .base import Base
from urllib.request import urlopen, Request


class Facepalm(Base):
    name = 'facepalm'
    aliases = ['o']

    @staticmethod
    def execute(bot, command):
        req = Request("http://loremflickr.com/500/410/facepalm", headers={'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"})
        output = open("storage/facepalm.jpg", "wb")
        output.write(urlopen(req).read())
        output.close()

        bot.send_photo(chat_id=command.chat_id, photo=open('storage/facepalm.jpg', 'rb'))
