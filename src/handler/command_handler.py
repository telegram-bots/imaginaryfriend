import random
import logging

from telegram import Update
from telegram.ext import Handler

from src.domain.command import Command
from src.entity.pair import Pair
from .moderate_command import ModerateCommand


class CommandHandler(Handler):
    def __init__(self, chance_manager):
        super(CommandHandler, self).__init__(self.handle)
        self.commands = {
            'start':      self.__start_command,
            'help':       self.__help_command,
            'ping':       self.__ping_command,
            'set_chance': self.__set_chance_command,
            'get_chance': self.__get_chance_command,
            'get_stats':  self.__get_stats_command,
            'moderate':   self.__moderate_command
        }
        self.chance_manager = chance_manager

    def check_update(self, update):
        if isinstance(update, Update) and update.message:
            message = update.message

            return message.text and message.text.startswith('/') and Command.parse_name(message) in self.commands
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
            self.__reply(bot, command, 'Invalid command! Type /help')
            
    def __reply(self, bot, command, message):
        logging.debug("[Chat %s %s command] %s: %s" %
                      (command.chat_type,
                       command.chat_id,
                       command.name,
                       message))

        bot.send_message(chat_id=command.chat_id,
                         reply_to_message_id=command.message.message_id,
                         text=message)

    def __start_command(self, bot, command):
        self.__reply(bot, command, 'Hi! :3')

    def __help_command(self, bot, command):
        self.__reply(
            bot,
            command,
            """Add me to your group and let me listen to your chat for a while.
When I learn enough word pairs, I'll start bringing fun and absurdity to your conversations.

Available commands:
• /ping,
• /get_stats: get the number of word pairs I've learned in this chat,
• /set_chance: set the chance that I'll reply to a random message (must be in range 1-50, default: 5),
• /get_chance: get the current chance of my random reply.

If you get tired of me, you can kick me from the group.
In 12 hours, I'll forget everything that have been learned in your chat, so you can add me again and teach me new things!
"""
        )

    def __ping_command(self, bot, command):
        answers = [
            'echo',
            'pong',
            'ACK',
            'reply',
            'pingback'
        ]

        self.__reply(bot, command, random.choice(answers))

    def __set_chance_command(self, bot, command):
        try:
            chance = int(command.args[0])

            if chance < 1 or chance > 50:
                raise ValueError

            self.chance_manager.set_chance(chat_id=command.chat_id, chance=chance)

            self.__reply(bot, command, 'Set chance to: {}'.format(chance))
        except (IndexError, ValueError):
            self.__reply(bot, command, 'Usage: /set_chance 1-50.')

    def __get_chance_command(self, bot, command):
        self.__reply(bot, command, 'Current chance: {}'
                     .format(self.chance_manager.get_chance(command.chat_id)))

    def __get_stats_command(self, bot, command):
        self.__reply(bot, command, 'Pairs: {}'
                     .format(Pair.where('chat_id', command.chat_id).count()))

    def __moderate_command(self, bot, command):
        try:
            moderate = ModerateCommand(bot, command)

            if not moderate.is_admin():
                return self.__reply(bot, command, 'You don\'t have admin privileges!')

            if len(command.args) == 2:
                moderate.remove_word(command.args[1])
            else:
                self.__reply(bot, command, moderate.find_similar_words(command.args[0]))
        except (IndexError, ValueError):
            self.__reply(bot, command, """Usage:
/moderate <word> for search
/moderate <word> <word_id> for deletion""")

