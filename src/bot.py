import logging

from telegram.ext import Updater
from src.command_handler import CommandHandler
from src.message_handler import MessageHandler


class Bot:
    def __init__(self, config):
        self.config = config
        self.updater = Updater(token=config['bot']['token'])
        self.dispatcher = self.updater.dispatcher

    def run(self):
        logging.info("Bot started")
        message_handler = MessageHandler(self.config)
        command_handler = CommandHandler()

        self.dispatcher.add_handler(message_handler)
        self.dispatcher.add_handler(command_handler)
        self.updater.start_polling()
        self.updater.idle()
