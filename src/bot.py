import logging

from telegram.ext import Updater
from src.handlers.message_handler import MessageHandler
from src.handlers.command_handler import CommandHandler
from src.handlers.status_handler import StatusHandler
from . import chat_purge_queue


class Bot:
    def __init__(self, config):
        self.config = config
        self.updater = Updater(token=config['bot']['token'])
        self.dispatcher = self.updater.dispatcher

    def run(self):
        logging.info("Bot started")

        chat_purge_queue.init(
            queue=self.updater.job_queue,
            default_interval=self.config['bot']['purge_interval']
        )

        self.dispatcher.add_handler(MessageHandler(self.config))
        self.dispatcher.add_handler(CommandHandler(self.config))
        self.dispatcher.add_handler(StatusHandler(self.config))

        self.updater.start_polling()
        self.updater.idle()
