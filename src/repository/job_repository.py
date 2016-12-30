from . import RedisRepository
from src.config import encoding
import json
from datetime import datetime
from typing import Iterator


class JobRepository(RedisRepository):
    def __init__(self):
        RedisRepository.__init__(self, source_name='jobs')

    def add(self, chat_id: int, dt: datetime) -> None:
        self.redis.instance().hset(
            self.source_name,
            chat_id,
            json.dumps({'chat_id': chat_id, 'execute_at': dt.timestamp()})
        )

    def delete(self, chat_id: int) -> None:
        self.redis.instance().hdel(self.source_name, chat_id)

    def get_all(self) -> Iterator[object]:
        return map(lambda j: json.loads(j.decode(encoding)),
                   self.redis.instance().hgetall(self.source_name).values())
