from . import BaseRepository
from src.config import redis, encoding


class RedisRepository(BaseRepository):
    def __init__(self, source_name: str):
        self.redis = redis
        self.source_name = source_name

    def to_int(self, byte: bytes, default: int) -> int:
        if byte is None:
            return default

        return int(byte.decode(encoding))
