import logging.config
import configparser

from src.bot import Bot


def main():
    config = get_config('./main.cfg')
    logging.basicConfig(level=config['logging']['level'])
    Bot(config).run()


def get_config(path):
    config = configparser.ConfigParser()
    config.read(path)
    return config

if __name__ == '__main__':
    main()
