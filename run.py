import logging.config
import configparser

from src.bot import Bot
from orator.orm import Model
from orator import DatabaseManager


def main():
    config = configparser.ConfigParser()
    config.read('./main.cfg', encoding='utf-8')

    logging.basicConfig(level=config['logging']['level'])
    logging.getLogger("telegram.bot").setLevel(logging.ERROR)
    logging.getLogger("telegram.ext").setLevel(logging.ERROR)

    Model.set_connection_resolver(DatabaseManager({'db': config['db']}))

    Bot(config).run()

if __name__ == '__main__':
    main()
