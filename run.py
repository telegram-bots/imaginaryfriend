import logging.config
import configparser

from src.bot import Bot


def main():
    config = configparser.ConfigParser()
    config.read('./main.cfg')
    logging.basicConfig(level=config['logging']['level'])
    Bot(config).run()

if __name__ == '__main__':
    main()
