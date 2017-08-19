from . import RedisRepository
from src.component.config import encoding
import json


class JobRepository(RedisRepository):
    def __init__(self):
        RedisRepository.__init__(self, source_name='jobs')

    def add(self, chat_id, datetime):
        self.redis.instance().hset(
            self.source_name,
            chat_id,
            json.dumps({'chat_id': chat_id, 'execute_at': datetime.timestamp()})
        )

    def delete(self, chat_id):
        self.redis.instance().hdel(self.source_name, chat_id)

    def get_all(self):
        return map(lambda j: json.loads(j.decode(encoding)),
                   self.redis.instance().hgetall(self.source_name).values())
