import logging

from telegram.ext import Updater

from src.config import config
from src.handler.command_handler import CommandHandler
from src.handler.message_handler import MessageHandler
from src.handler.status_handler import StatusHandler
from src.service.chat_purge_queue import ChatPurgeQueue
from src.service.data_learner import DataLearner
from src.service.message_sender import MessageSender
from src.service.reply_generator import ReplyGenerator


class Bot:
    def __init__(self):
        self.updater = Updater(token=config['bot']['token'])
        self.dispatcher = self.updater.dispatcher

    def run(self):
        logging.info("Bot started")

        message_sender = MessageSender(self.dispatcher.bot)

        self.dispatcher.add_handler(MessageHandler(message_sender=message_sender,
                                                   data_learner=DataLearner(),
                                                   reply_generator=ReplyGenerator()))
        self.dispatcher.add_handler(CommandHandler(message_sender=message_sender))
        self.dispatcher.add_handler(StatusHandler(chat_purge_queue=ChatPurgeQueue(self.updater.job_queue)))

        self.updater.start_polling()
        self.updater.idle()
