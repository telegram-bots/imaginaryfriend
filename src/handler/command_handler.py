import random
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import Handler

from src.entity.chat import Chat
from src.domain.command import Command
from src.entity.word import Word


class CommandHandler(Handler):
    def __init__(self, message_sender):
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
        self.message_sender = message_sender

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
        chat = Chat.get_chat(update.message)
        command = Command(chat=chat, message=update.message)

        try:
            self.commands[command.name](bot, command)
        except (IndexError, ValueError):
            self.message_sender.reply(command, 'Invalid command! Type /help')

    def __start_command(self, bot, command):
        self.message_sender.reply(command, 'Hi! :3')

    def __help_command(self, bot, command):
        self.message_sender.reply(
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

        self.message_sender.reply(command, random.choice(answers))

    def __set_chance_command(self, bot, command):
        try:
            random_chance = int(command.args[0])

            if random_chance < 1 or random_chance > 50:
                raise ValueError

            command.chat.update(random_chance=random_chance)

            self.message_sender.reply(command, 'Set chance to: {}'.format(random_chance))
        except (IndexError, ValueError):
            self.message_sender.reply(command, 'Usage: /set_chance 1-50.')

    def __get_chance_command(self, bot, command):
        self.message_sender.reply(command, 'Current chance: {}'.format(command.chat.random_chance))

    def __get_stats_command(self, bot, command):
        self.message_sender.reply(command, 'Pairs: {}'.format(command.chat.pairs().count()))

    def __moderate_command(self, bot, command):
        try:
            def is_admin():
                user_id = command.message.from_user.id
                admin_ids = list(map(
                    lambda member: member.user.id,
                    bot.get_chat_administrators(chat_id=command.chat.telegram_id)
                ))

                return user_id in admin_ids

            def generate_keyboard(words):
                custom_keyboard = []
                for word in words:
                    custom_keyboard.append([
                        InlineKeyboardButton(text=word.word, callback_data='nothing'),
                        InlineKeyboardButton(text='🔲', callback_data=word.id)
                    ])

                custom_keyboard.append([
                    InlineKeyboardButton(text='Cancel', callback_data='cancel'),
                    InlineKeyboardButton(text='OK', callback_data='remove_all_marked_words')
                ])

                return InlineKeyboardMarkup(custom_keyboard)

            if not is_admin():
                return self.message_sender.reply(command, 'You don\'t have admin privileges!')

            search_word = command.args[0]
            found_words = Word.where('word', 'like', search_word + '%') \
                .order_by('word', 'asc') \
                .limit(10) \
                .get()

            if len(found_words) == 0:
                self.message_sender.reply(command, 'No words found!')
            else:
                self.message_sender.send_reply_markup(command,
                                                      message="Mark all words to delete and press OK, "
                                                              "or press Cancel to close this window",
                                                      reply_markup=generate_keyboard(found_words))
        except (IndexError, ValueError):
            self.message_sender.reply(command, 'Usage: /moderate <word>')

