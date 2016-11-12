import configparser
from src.chat_purge_queue import ChatPurgeQueue

config = configparser.ConfigParser()
config.read('./main.cfg', encoding='utf-8')
