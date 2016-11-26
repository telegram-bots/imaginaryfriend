from datetime import datetime, timedelta
from src.config import config


class LinksChecker:
    def __init__(self, redis):
        self.redis = redis

    def check(self, chat_id, links):
        """Returns True if atleast one link already exists
        """

        redis = self.redis.instance()
        key = "links:{}".format(chat_id)
        now = datetime.now()
        delete_at = (now + timedelta(seconds=float(config['redis']['links_lifetime']))).timestamp()

        # Delete stale links
        redis.zremrangebyscore(key, 0, now.timestamp())

        # Update links timestamps
        pipe = redis.pipeline()
        for link in links:
            pipe.zadd(key, link, delete_at)

        return any(x == 0 for x in pipe.execute())
