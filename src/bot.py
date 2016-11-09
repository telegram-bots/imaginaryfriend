import logging

from telegram.ext import Updater
from telegram.ext import MessageHandler, CommandHandler, Filters
from orator.orm import Model
from orator import DatabaseManager
from src.message import Message
from src.command_manager import CommandManager


class Bot:
    def __init__(self, config):
        self.config = config
        self.updater = Updater(token=config['bot']['token'])
        self.dispatcher = self.updater.dispatcher
        self.command_manager = CommandManager()

        Model.set_connection_resolver(DatabaseManager({'db': config['db']}))

    def message_handler(self, bot, update):
        Message(bot=bot, message=update.message, config=self.config).process()

    def command_handler(self, bot, update, args):
        try:
            command = update.message.text.strip('/').split(' ')[0]

            self.command_manager.handle(bot=bot, update=update, command=command, args=args)
        except (IndexError, ValueError):
            update.message.reply_text('Invalid command!')

    def run(self):
        logging.info("Bot started")
        message_handler = MessageHandler(Filters.text, self.message_handler)
        command_handler = CommandHandler('set_chance', self.command_handler, pass_args=True)

        self.dispatcher.add_handler(message_handler)
        self.dispatcher.add_handler(command_handler)
        self.updater.start_polling()
        self.updater.idle()
