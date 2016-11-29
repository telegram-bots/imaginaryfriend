from datetime import datetime, timedelta
from src.config import config


class LinksChecker:
    def __init__(self, redis):
        self.redis = redis
        self.lifetime = timedelta(seconds=config.getfloat('links', 'lifetime'))

    def check(self, chat_id, links):
        """Returns True if at least one link already exists
        """

        redis = self.redis.instance()
        key = "links:{}".format(chat_id)
        now = datetime.now()
        delete_at = (now + self.lifetime).timestamp()

        redis.zremrangebyscore(key, 0, now.timestamp())

        pipe = redis.pipeline()
        for link in links:
            pipe.zadd(key, link, delete_at)

        return any(x == 0 for x in pipe.execute())
