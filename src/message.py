from src.domain import (Chat, Pair)
import logging
import random


class Message:
    def __init__(self, bot, message, config):
        self.bot = bot
        self.message = message
        self.config = config
        self.chat = Chat.get_chat(message)
        self.chat.migrate_to_chat_id = message.migrate_to_chat_id

        if self.has_text():
            logging.debug("[chat %s %s bare_text] %s" %(self.chat.chat_type, self.chat.telegram_id, self.message.text))
            self.text = message.text
            self.words = self.__get_words()
            self.command = self.__get_command() if self.text[0] == '/' else None

    def process(self):
        if self.has_text() and not self.is_editing():
            # TODO Implement
            if self.is_command():
                pass
            else:
                return self.__process_message()

    def has_text(self):
        return self.message.text != ''

    def is_editing(self):
        return self.message.edit_date is not None

    def has_entities(self):
        return self.message.entities is not None

    def has_anchors(self):
        return self.has_text() and (any(x in self.words for x in self.config['bot']['anchors'].split(',')))

    def is_private(self):
        return self.message.chat.type == 'private'

    def is_reply_to_bot(self):
        return self.message.reply_to_message.from_user.username == self.config['bot']['name']

    def is_random_answer(self):
        return random.randint(1, 100) < self.chat.random_chance

    def is_command(self):
        return self.command is not None

    def __answer(self, message):
        logging.debug("[Chat %s %s answer] %s" % (self.chat.chat_type, self.chat.telegram_id, message))
        self.bot.sendMessage(chat_id=self.chat.telegram_id, text=message)

    def __reply(self, message):
        logging.debug("[Chat %s %s reply] %s" % (self.chat.chat_type, self.chat.telegram_id, message))
        self.bot.sendMessage(chat_id=self.chat.telegram_id, reply_to_message_id=self.message.message_id, text=message)

    def __process_message(self):
        Pair.learn(self)

        if self.has_anchors() or self.is_private() or self.is_reply_to_bot() or self.is_random_answer():
            reply = Pair.generate(self)
            if reply != '':
                self.__answer(reply)

    def __get_words(self):
        text = self.text
        for entity in self.message.entities:
            text[entity.offset, entity.length] = ' ' * entity.length
        result = map(lambda x: x.lower(), text.split(' '))
        logging.debug("[chat %s %s get_words] %s" % (self.chat.chat_type, self.chat.telegram_id, result))

        return result

    # TODO Implement
    def __get_command(self):
        return None
