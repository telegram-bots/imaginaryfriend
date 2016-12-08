from telegram import Update
from telegram.ext import Handler

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

    def handle(self, bot, update):
        command = Command(update.message)

        try:
            self.commands[command.name](bot, command)
        except (IndexError, ValueError):
            bot.send_message(chat_id=command.chat_id,
                             reply_to_message_id=command.message.message_id,
                             text='Invalid command! Type /help')
