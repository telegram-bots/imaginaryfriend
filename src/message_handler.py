import logging

from telegram.ext import MessageHandler as ParentHandler, Filters

from src.domain.message import Message
from src.domain.pair import Pair


class MessageHandler(ParentHandler):
    def __init__(self,
                 config,
                 allow_edited=False,
                 pass_update_queue=False,
                 pass_user_data=False,
                 pass_chat_data=False):
        super(MessageHandler, self).__init__(
            Filters.text | Filters.sticker | Filters.status_update,
            self.handle,
            pass_update_queue=pass_update_queue,
            pass_job_queue=True,
            pass_user_data=pass_user_data,
            pass_chat_data=pass_chat_data,
            allow_edited=allow_edited)

        self.config = config

    def handle(self, bot, update, job_queue):
        print(job_queue)
        message = Message(message=update.message, config=self.config)

        if message.has_text():
            logging.debug("[Chat %s %s bare_text] %s" %
                          (message.chat.chat_type,
                           message.chat.telegram_id,
                           message.text))

        if message.has_text() and not (message.is_editing() or message.is_command()):
            return self.__process_message(bot, message)
        elif message.is_sticker():
            return self.__process_sticker(bot, message)
        elif message.is_bot_added():
            return self.__process_bot_add(bot, message)
        elif message.is_bot_kicked():
            return self.__process_bot_kick(bot, message)

    def __process_message(self, bot, message):
        Pair.learn(message)

        if message.has_anchors() \
                or message.is_private() \
                or message.is_reply_to_bot() \
                or message.is_random_answer():

            reply = Pair.generate(message)
            if reply != '':
                self.__answer(bot, message, reply)

    def __process_sticker(self, bot, message):
        if message.has_anchors() \
                or message.is_private() \
                or message.is_reply_to_bot() \
                or message.is_random_answer():

            self.__send_sticker(bot, message, "BQADAgADSAIAAkcGQwU-G-9SZUDTWAI")

    def __process_bot_kick(self, bot, message):
        logging.debug("[Chat %s %s bot_kicked]" %
                      (message.chat.chat_type, message.chat.telegram_id))

    def __process_bot_add(self, bot, message):
        logging.debug("[Chat %s %s bot_added]" %
                      (message.chat.chat_type, message.chat.telegram_id))

    def __answer(self, bot, message, reply):
        logging.debug("[Chat %s %s answer] %s" %
                      (message.chat.chat_type,
                       message.chat.telegram_id,
                       reply))

        bot.sendMessage(chat_id=message.chat.telegram_id, text=reply)

    def __reply(self, bot, message, reply):
        logging.debug("[Chat %s %s reply] %s" %
                      (message.chat.chat_type,
                       message.chat.telegram_id,
                       reply))

        bot.sendMessage(chat_id=message.chat.telegram_id,
                        reply_to_message_id=message.message.message_id,
                        text=reply)

    def __send_sticker(self, bot, message, sticker_id):
        logging.debug("[Chat %s %s send_sticker]" %
                      (message.chat.chat_type, message.chat.telegram_id))

        bot.sendSticker(chat_id=message.chat.telegram_id,
                        reply_to_message_id=message.message.message_id,
                        sticker=sticker_id)
