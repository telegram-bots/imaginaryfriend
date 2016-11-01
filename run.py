import logging.config
import configparser

from src.bot import Bot


def main():
    config = configparser.ConfigParser()
    config.read('./main.cfg', encoding='utf-8')
    logging.basicConfig(level=config['logging']['level'])
    Bot(config).run()

if __name__ == '__main__':
    main()
