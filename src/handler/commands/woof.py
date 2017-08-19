from .base import Base
from urllib.request import urlopen, Request


class Woof(Base):
    name = 'woof'
    path = 'storage/woof.jpg'
    headers = {'User-Agent': "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/53.0.2785.143 Safari/537.36"}

    def execute(self, command):
        req = Request("http://loremflickr.com/500/410/dog", headers=self.headers)
        output = open(self.path, "wb")
        output.write(urlopen(req).read())
        output.close()

        self.send_photo(command, photo=open(self.path, 'rb'))
