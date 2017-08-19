from .base import Base
import json
import random
from urllib.request import urlopen


class XKCD(Base):
    name = 'xkcd'

    def execute(self, command):
        last_id = json.loads(urlopen("http://xkcd.com/info.0.json").read().decode('utf-8'))['num']
        random_id = random.randint(1, last_id)
        req = urlopen('http://xkcd.com/%d/info.0.json' % random_id)
        data = json.loads(req.read().decode('utf-8'))

        self.send_photo(command, photo=data['img'])
