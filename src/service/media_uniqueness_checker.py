from datetime import datetime, timedelta
from src.config import config, redis
from urllib.parse import urlparse


class MediaUniquenessChecker:
    def __init__(self):
        self.redis = redis
        self.key = "media_checker:{}"
        self.lifetime = timedelta(seconds=config.getfloat('media_checker', 'lifetime'))

    def check(self, message):
        """Returns True if at least one media entity was already in this chat
        """

        redis = self.redis.instance()
        key = self.key.format(message.chat_id)
        now = datetime.now()
        delete_at = (now + self.lifetime).timestamp()

        redis.zremrangebyscore(key, 0, now.timestamp())

        pipe = redis.pipeline()
        for element in self.__extract_media(message):
            pipe.zadd(key, element, delete_at)

        return any(x == 0 for x in pipe.execute())

    def __extract_media(self, message):
        media = []

        def prettify(url):
            if not url.startswith('http://') and not url.startswith('https://'):
                url = 'http://' + url

            link = urlparse(url)
            host = '.'.join(link.hostname.split('.')[-2:])
            return '{}{}#{}?{}'.format(host, link.path, link.fragment, link.query)

        for entity in filter(lambda e: e.type == 'url', message.message.entities):
            link = prettify(message.text[entity.offset:entity.length + entity.offset])
            media.append(link)

        media += list(map(lambda p: p.file_id, getattr(message.message, 'photo', [])))

        return media
