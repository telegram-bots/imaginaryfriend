import redis
from redis.exceptions import BusyLoadingError
from retry import retry


class Redis:
    """
    Small redis wrapper, to simplify work with connection pool
    """
    def __init__(self, config):
        self.pool = redis.ConnectionPool(host=config['redis']['host'],
                                         port=config.getint('redis', 'port'),
                                         db=config['redis']['db'])
        self.__ensure_dataset_loaded()

    def instance(self):
        return redis.Redis(connection_pool=self.pool)

    @retry(BusyLoadingError, tries=5, delay=10, logger=None)
    def __ensure_dataset_loaded(self):
        self.instance().ping()
