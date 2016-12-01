import logging

from telegram.ext import Updater

from src.config import config
from src.redis_c import Redis
from src.handler.command_handler import CommandHandler
from src.handler.message_handler import MessageHandler
from src.handler.status_handler import StatusHandler
from src.service.chat_purge_queue import ChatPurgeQueue
from src.service.data_learner import DataLearner
from src.service.reply_generator import ReplyGenerator
from src.service.links_checker import LinksChecker
from src.service.chance_manager import ChanceManager


class Bot:
    def __init__(self):
        self.updater = Updater(token=config['bot']['token'])
        self.dispatcher = self.updater.dispatcher

    def run(self):
        logging.info("Bot started")

        redis = Redis(config)
        chance_manager = ChanceManager(redis)

        self.dispatcher.add_handler(MessageHandler(data_learner=DataLearner(),
                                                   reply_generator=ReplyGenerator(),
                                                   links_checker=LinksChecker(redis),
                                                   chance_manager=chance_manager))
        self.dispatcher.add_handler(CommandHandler(chance_manager=chance_manager))
        self.dispatcher.add_handler(StatusHandler(chat_purge_queue=ChatPurgeQueue(self.updater.job_queue, redis)))

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
