import logging

from telegram.ext import Updater
from telegram.ext import MessageHandler, Filters
from orator.orm import Model
from orator import DatabaseManager
from src.message import Message
from src.command_handler import CommandHandler


class Bot:
    def __init__(self, config):
        self.config = config
        self.updater = Updater(token=config['bot']['token'])
        self.dispatcher = self.updater.dispatcher

        Model.set_connection_resolver(DatabaseManager({'db': config['db']}))

    def message_handler(self, bot, update):
        Message(bot=bot, message=update.message, config=self.config).process()

    def run(self):
        logging.info("Bot started")
        message_handler = MessageHandler(Filters.text, self.message_handler)
        command_handler = CommandHandler()

        self.dispatcher.add_handler(message_handler)
        self.dispatcher.add_handler(command_handler)
        self.updater.start_polling()
        self.updater.idle()
