import logging.config

from src.bot import Bot
from orator.orm import Model
from orator import DatabaseManager
from src import config


def main():
    logging.basicConfig(level=config['logging']['level'])
    logging.getLogger("telegram.bot").setLevel(logging.ERROR)
    logging.getLogger("telegram.ext").setLevel(logging.ERROR)

    Model.set_connection_resolver(DatabaseManager({'db': config['db']}))

    Bot().run()

if __name__ == '__main__':
    main()
