import logging

from random import choice
from src.config import config, data_learner, reply_generator, media_checker, chance_manager
from telegram.ext import MessageHandler as ParentHandler, Filters
from telegram import ChatAction
from src.domain.message import Message


class MessageHandler(ParentHandler):
    def __init__(self):
        super(MessageHandler, self).__init__(
            Filters.text | Filters.sticker | Filters.photo,
            self.handle)
        self.data_learner = data_learner
        self.reply_generator = reply_generator
        self.media_checker = media_checker
        self.chance_manager = chance_manager
        self.spam_stickers = config.getlist('bot', 'spam_stickers')
        self.media_checker_messages = config.getlist('media_checker', 'messages')

    def handle(self, bot, update):
        chance = self.chance_manager.get_chance(update.message.chat.id)
        message = Message(chance=chance, message=update.message)

        self.__check_media_uniqueness(bot, message)

        if message.has_text() and not message.is_editing():
            self.__process_message(bot, message)
        elif message.is_sticker():
            self.__process_sticker(bot, message)

    def __check_media_uniqueness(self, bot, message):
        if not message.is_private()\
                and message.has_entities()\
                and self.media_checker.check(message):
            logging.debug("[Chat %s %s not unique media]" %
                          (message.chat_type,
                           message.chat_id))

            bot.send_message(chat_id=message.chat_id,
                             reply_to_message_id=message.message.message_id,
                             text=choice(self.media_checker_messages))

    def __process_message(self, bot, message):
        logging.debug("[Chat %s %s message length] %s" %
                      (message.chat_type,
                       message.chat_id,
                       len(message.text)))

        should_answer = message.should_answer()

        if should_answer:
            bot.send_chat_action(chat_id=message.chat_id, action=ChatAction.TYPING)

        self.data_learner.learn(message)

        if should_answer:
            text = self.reply_generator.generate(message)
            reply_id = None if not message.is_reply_to_bot() else message.message.message_id

            logging.debug("[Chat %s %s answer/reply] %s" %
                          (message.chat_type,
                           message.chat_id,
                           text))

            bot.send_message(chat_id=message.chat_id,
                             reply_to_message_id=reply_id,
                             text=text)

    def __process_sticker(self, bot, message):
        if message.has_anchors() \
                or message.is_private() \
                or message.is_reply_to_bot():
            logging.debug("[Chat %s %s spam_sticker]" %
                          (message.chat_type,
                           message.chat_id))

            bot.send_sticker(chat_id=message.chat_id,
                             reply_to_message_id=message.message.message_id,
                             sticker=choice(self.spam_stickers))
