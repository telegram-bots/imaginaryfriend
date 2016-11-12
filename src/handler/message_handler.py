import logging

from telegram.ext import MessageHandler as ParentHandler, Filters

from src.domain.message import Message
from src.entity.chat import Chat


class MessageHandler(ParentHandler):
    def __init__(self, data_learner, reply_generator):
        super(MessageHandler, self).__init__(
            Filters.text | Filters.sticker,
            self.handle)

        self.data_learner = data_learner
        self.reply_generator = reply_generator

    def handle(self, bot, update):
        chat = Chat.get_chat(update.message)
        message = Message(chat=chat, message=update.message)

        if message.has_text():
            logging.debug("[Chat %s %s bare_text] %s" %
                          (message.chat.chat_type,
                           message.chat.telegram_id,
                           message.text))

        if message.has_text() and not message.is_editing():
            return self.__process_message(bot, message)
        elif message.is_sticker():
            return self.__process_sticker(bot, message)

    def __process_message(self, bot, message):
        self.data_learner.learn(message)

        if message.has_anchors() \
                or message.is_private() \
                or message.is_reply_to_bot() \
                or message.is_random_answer():
            reply = self.reply_generator.generate(message)
            if reply != '':
                self.__answer(bot, message, reply)

    def __process_sticker(self, bot, message):
        if message.has_anchors() \
                or message.is_private() \
                or message.is_reply_to_bot() \
                or message.is_random_answer():

            self.__send_sticker(bot, message, "BQADAgADSAIAAkcGQwU-G-9SZUDTWAI")

    def __answer(self, bot, message, reply):
        logging.debug("[Chat %s %s answer] %s" %
                      (message.chat.chat_type,
                       message.chat.telegram_id,
                       reply))

        bot.sendMessage(chat_id=message.chat.telegram_id, text=reply)

    def __send_sticker(self, bot, message, sticker_id):
        logging.debug("[Chat %s %s send_sticker]" %
                      (message.chat.chat_type, message.chat.telegram_id))

        bot.sendSticker(chat_id=message.chat.telegram_id,
                        reply_to_message_id=message.message.message_id,
                        sticker=sticker_id)
