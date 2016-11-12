from telegram import Update
from telegram.ext import Handler

from src.entity.chat import Chat
from src.domain.command import Command


class CommandHandler(Handler):
    def __init__(self):
        super(CommandHandler, self).__init__(self.handle)
        self.commands = {
            'start':      self.__start_command,
            'help':       self.__help_command,
            'ping':       self.__ping_command,
            'set_chance': self.__set_chance_command,
            'get_chance': self.__get_chance_command,
            'get_stats':  self.__get_stats_command
        }
    
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
        try:
            chat = Chat.get_chat(update.message)
            command = Command(chat=chat, message=update.message)

            callback = self.commands[command.name]
            callback(update, command)
        except (IndexError, ValueError):
            update.message.reply_text('Invalid command! Type /help')
    
    def __start_command(self, update, command):
        update.message.reply_text('Hi! :3')
        
    def __help_command(self, update, command):
        update.message.reply_text(
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

    def __ping_command(self, update, command):
        update.message.reply_text('pong')

    def __set_chance_command(self, update, command):
        try:
            random_chance = int(command.args[0])

            if random_chance < 1 or random_chance > 50:
                raise ValueError

            command.chat.update(random_chance=random_chance)

            update.message.reply_text('Set chance to: {}'.format(random_chance))
        except (IndexError, ValueError):
            update.message.reply_text('Usage: /set_chance 1-50.')
                                  
    def __get_chance_command(self, update, command):
        update.message.reply_text('Current chance: {}'.format(command.chat.random_chance))
                                  
    def __get_stats_command(self, update, command):
        update.message.reply_text('Pairs: {}'.format(command.chat.pairs().count()))
