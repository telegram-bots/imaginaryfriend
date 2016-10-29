import logging
import random
import urllib.request
import sqlite3

from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from orator import DatabaseManager, Model
from src.domain.message import Message


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
        self.create_table()

    def create_table(self):
        connection = sqlite3.connect(self.config['db']['database'])
        cursor = connection.cursor()
        cursor.execute('''CREATE TABLE IF NOT EXISTS messages
             (id INTEGER PRIMARY KEY,
             chat_id text,
             user_name text,
             user_id text,
             payload text,
             created_at TIMESTAMP,
             updated_at TIMESTAMP)''')
        connection.commit()
        connection.close()

    def handler(self, bot, update):
        Message.create(chat_id=update.message.chat_id,
                       user_name=update.message.from_user.username,
                       user_id=update.message.from_user.id,
                       payload=update.message.text)

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
