import logging
import random
import urllib.request

from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from orator.orm import Model
from orator import DatabaseManager

class Bot:
    messages = [
        'Я кот, нееште меня!',
        'Не обижайте пиздюка!',
        'Ты няшка :3',
        'Всем по котейке!',
        'Юра, го бильярд',
        'Бога нет.',
    ]

    def __init__(self, config):
        self.config = config
        self.updater = Updater(token=config['bot']['token'])
        self.dispatcher = self.updater.dispatcher

        Model.set_connection_resolver(DatabaseManager({'db': config['db']}))

    def handler(self, bot, update):
        value = random.randint(0, 2)
        if value == 1:
            message = random.choice(self.messages)
            logging.debug("Sending random message: " + message)
            bot.sendMessage(chat_id=update.message.chat_id, text=message)
        elif value == 2:
            message = update.message.text
            logging.debug("Mirroring message: " + message)
            bot.sendMessage(chat_id=update.message.chat_id, text=message)
        else:
            opener = urllib.request.build_opener(urllib.request.HTTPRedirectHandler)
            request = opener.open('http://thecatapi.com/api/images/get?format=src')
            url = request.url
            logging.debug("Sending random cat picture: " + url)
            bot.sendPhoto(chat_id=update.message.chat_id, photo=url)

    def run(self):
        logging.info("Bot started")
        handler = MessageHandler([Filters.text], self.handler)
        self.dispatcher.add_handler(handler)
        self.updater.start_polling()
