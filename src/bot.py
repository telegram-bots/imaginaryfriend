import logging

from telegram.ext import Updater

from src.config import config, chat_purge_queue
from src.handler import *


class Bot:
    """
    Main initializer and dispatcher of messages
    """
    def __init__(self):
        self.updater = Updater(token=config['bot']['token'])
        self.dispatcher = self.updater.dispatcher

    def run(self):
        logging.info("Bot started")

        purge_queue_instance = chat_purge_queue.instance(self.updater.job_queue)

        self.dispatcher.add_handler(MessageHandler())
        self.dispatcher.add_handler(CommandHandler())
        self.dispatcher.add_handler(StatusHandler(chat_purge_queue=purge_queue_instance))

        if config['updates']['mode'] == 'polling':
            self.updater.start_polling()
        elif config['updates']['mode'] == 'webhook':
            key = open(config['updates']['key'], 'rb') if config['updates']['key'] is not None else None
            cert = open(config['updates']['cert'], 'rb') if config['updates']['cert'] is not None else None

            self.updater.start_webhook(listen=config['updates']['host'],
                                       port=config.getint('updates', 'port'),
                                       url_path=config['bot']['token'],
                                       key=key,
                                       cert=cert,
                                       webhook_url=config['updates']['url'])

        self.updater.idle()
