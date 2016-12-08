import redis


class Redis:
    def __init__(self, config):
        self.pool = redis.ConnectionPool(host=config['redis']['host'],
                                         port=config.getint('redis', 'port'),
                                         db=config['redis']['db'])

    def instance(self):
        return redis.Redis(connection_pool=self.pool)
