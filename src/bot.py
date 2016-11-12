import logging

from telegram.ext import Updater
from src.handlers.message_handler import MessageHandler
from src.handlers.command_handler import CommandHandler
from src.handlers.status_handler import StatusHandler
from src import ChatPurgeQueue
from . import config


class Bot:
    def __init__(self):
        self.updater = Updater(token=config['bot']['token'])
        self.dispatcher = self.updater.dispatcher

    def run(self):
        logging.info("Bot started")

        self.dispatcher.add_handler(MessageHandler())
        self.dispatcher.add_handler(CommandHandler())
        self.dispatcher.add_handler(StatusHandler(chat_purge_queue=ChatPurgeQueue(self.updater.job_queue)))

        self.updater.start_polling()
        self.updater.idle()
