from redis import Redis as Client, ConnectionPool
from configparser import ConfigParser


class Redis:
    """
    Small redis wrapper, to simplify work with connection pool
    """
    def __init__(self, config: ConfigParser):
        self.pool = ConnectionPool(host=config['redis']['host'],
                                   port=config.getint('redis', 'port'),
                                   db=config['redis']['db'])

    def instance(self) -> Client:
        return Client(connection_pool=self.pool)
