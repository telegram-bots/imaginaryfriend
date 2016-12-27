import logging.config

from src.bot import Bot
from src.config import config


def main():
    logging.basicConfig(level=config['logging']['level'])
    logging.getLogger("telegram.bot").setLevel(logging.ERROR)
    logging.getLogger("telegram.ext").setLevel(logging.ERROR)

    Bot().run()

if __name__ == '__main__':
    main()
