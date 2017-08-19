import logging
from telegram import Update
from telegram.ext import Handler
from telegram.ext.dispatcher import run_async

from src.domain.command import Command
from .commands import commands


class CommandHandler(Handler):
    def __init__(self):
        super(CommandHandler, self).__init__(self.handle)
        self.commands = commands

    def check_update(self, update):
        if isinstance(update, Update) and update.message:
            message = update.message

            return message.text \
                   and message.text.startswith('/') \
                   and Command.parse_name(message) in self.commands
        else:
            return False

    def handle_update(self, update, dispatcher):
        optional_args = self.collect_optional_args(dispatcher, update)

        return self.callback(dispatcher.bot, update, **optional_args)

    @run_async
    def handle(self, bot, update):
        data = Command(update.message)
        logging.debug(f"Incoming command: {data}")

        try:
            command = self.commands[data.name]
            if command.bot is None:
                command.bot = bot
            command.execute(data)
        except (KeyError, IndexError, ValueError):
            bot.send_message(
                chat_id=data.chat_id,
                reply_to_message_id=data.message.message_id,
                text='Invalid command! Type /help'
            )
