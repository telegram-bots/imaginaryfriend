import logging

from random import choice
from src.config import config
from telegram.ext import MessageHandler as ParentHandler, Filters
from telegram import ChatAction
from src.domain.message import Message


class MessageHandler(ParentHandler):
    def __init__(self, data_learner, reply_generator, links_checker, chance_manager):
        super(MessageHandler, self).__init__(
            Filters.text | Filters.sticker,
            self.handle)

        self.data_learner = data_learner
        self.reply_generator = reply_generator
        self.links_checker = links_checker
        self.chance_manager = chance_manager

    def handle(self, bot, update):
        chance = self.chance_manager.get_chance(update.message.chat.id)
        message = Message(chance=chance, message=update.message)

        if message.has_text():
            logging.debug("[Chat %s %s bare_text] %s" %
                          (message.chat_type,
                           message.chat_id,
                           message.text))

        if message.has_text() and not message.is_editing():
            self.__process_message(bot, message)
        elif message.is_sticker():
            self.__process_sticker(bot, message)

    def __process_message(self, bot, message):
        should_answer = message.should_answer()

        if should_answer:
            bot.send_chat_action(chat_id=message.chat_id, action=ChatAction.TYPING)

        self.data_learner.learn(message)

        if message.has_links() and self.links_checker.check(message.chat_id, message.links):
            bot.send_sticker(chat_id=message.chat_id,
                             reply_to_message_id=message.message.message_id,
                             sticker=choice(config.getlist('links', 'stickers')))

        if should_answer:
            text = self.reply_generator.generate(message)
            reply_id = None if not message.is_reply_to_bot() else message.message.message_id

            logging.debug("[Chat %s %s answer] %s" %
                          (message.chat_type,
                           message.chat_id,
                           text))

            bot.send_message(chat_id=message.chat_id,
                             reply_to_message_id=reply_id,
                             text=text)

    def __process_sticker(self, bot, message):
        if message.should_answer():
            logging.debug("[Chat %s %s spam_sticker]" %
                          (message.chat_type,
                           message.chat_id))

            bot.send_sticker(chat_id=message.chat_id,
                             reply_to_message_id=message.message.message_id,
                             sticker=choice(config.getlist('bot', 'spam_stickers')))
