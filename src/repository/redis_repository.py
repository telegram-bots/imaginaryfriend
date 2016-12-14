from . import BaseRepository
from src.config import redis


class RedisRepository(BaseRepository):
    def __init__(self, source_name):
        self.redis = redis
        self.source_name = source_name

    def source(self, *args):
        return self.source_name.format(args)

    def to_int(self, byte, default):
        if byte is None:
            return default

        return int(byte.decode('utf-8'))
