import logging
from telegram import Update
from telegram.ext import Handler
from telegram.ext.dispatcher import run_async

from src.domain.command import Command
from .commands import command_handlers


class CommandHandler(Handler):
    def __init__(self):
        super(CommandHandler, self).__init__(self.handle)
        self.handlers = command_handlers

    def check_update(self, update):
        if isinstance(update, Update) and update.message:
            message = update.message

            return message.text \
                   and message.text.startswith('/') \
                   and Command.parse_name(message) in self.handlers
        else:
            return False

    def handle_update(self, update, dispatcher):
        optional_args = self.collect_optional_args(dispatcher, update)

        return self.callback(dispatcher.bot, update, **optional_args)

    @run_async
    def handle(self, bot, update):
        command = Command(update.message)
        logging.debug(f"Incoming command: {command}")

        handler = self.handlers[command.name]
        if handler.bot is None:
            handler.bot = bot
        handler.execute(command)
