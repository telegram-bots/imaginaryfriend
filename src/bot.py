import logging

from telegram.ext import Updater
from src.command_handler import CommandHandler
from src.message_handler import MessageHandler
from . import chat_purge_queue_handler


class Bot:
    def __init__(self, config):
        self.config = config
        self.updater = Updater(token=config['bot']['token'])
        self.dispatcher = self.updater.dispatcher

    def run(self):
        logging.info("Bot started")
        chat_purge_queue_handler.init(
            queue=self.updater.job_queue,
            default_interval=self.config['bot']['purge_interval']
        )

        message_handler = MessageHandler(self.config)
        command_handler = CommandHandler()

        self.dispatcher.add_handler(message_handler)
        self.dispatcher.add_handler(command_handler)
        self.updater.start_polling()
        self.updater.idle()
