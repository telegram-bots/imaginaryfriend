import logging
import random
import urllib.request

from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from orator.orm import Model
from orator import DatabaseManager
from src.message import Message


class Bot:
    # TODO Move and use
    # messages = [
    #     'Я кот, нееште меня!',
    #     'Не обижайте пиздюка!',
    #     'Ты няшка :3',
    #     'Всем по котейке!',
    #     'Юра, го бильярд',
    #     'Бога нет.',
    # ]

    def __init__(self, config):
        self.config = config
        self.updater = Updater(token=config['bot']['token'])
        self.dispatcher = self.updater.dispatcher

        Model.set_connection_resolver(DatabaseManager({'db': config['db']}))

    def handler(self, bot, update):
        Message(bot=bot, message=update.message, config=self.config).process()

    def run(self):
        logging.info("Bot started")
        handler = MessageHandler([Filters.text], self.handler)
        self.dispatcher.add_handler(handler)
        self.updater.start_polling()
