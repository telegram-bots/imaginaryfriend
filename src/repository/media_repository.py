from datetime import datetime, timedelta

from src.config import config
from . import RedisRepository


class MediaRepository(RedisRepository):
    def __init__(self):
        RedisRepository.__init__(self, source_name='media_checker:{}')
        self.lifetime = timedelta(seconds=config.getfloat('media_checker', 'lifetime'))

    def clear_stale_entries(self, chat_id, dt):
        """
        Remove all entries older than datetime (dt), for given chat_id
        :param chat_id: ID of chat
        :param dt: Datetime
        """
        self.redis \
            .instance() \
            .zremrangebyscore(self.source_name.format(chat_id), 0, dt.timestamp())

    def is_exists(self, chat_id, media_list):
        """
        Checks that at least one media entry is already in storage
        :param chat_id: ID of chat
        :param media_list: List of media entries
        :return: True, if at least one media entry already exists in storage
        """
        delete_at = (datetime.now() + self.lifetime).timestamp()
        pipe = self.redis.instance().pipeline()
        key = self.source_name.format(chat_id)

        for media in media_list:
            pipe.zadd(key, media, delete_at)

        return any(x == 0 for x in pipe.execute())
