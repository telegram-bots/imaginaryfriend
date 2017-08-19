import logging
from .base import Base
from telegram import ChatAction
from src.config import data_learner, reply_generator


class MessageProcessor(Base):
    def __init__(self):
        super().__init__()
        self.data_learner = data_learner
        self.reply_generator = reply_generator

    def can_handle(self, message):
        return message.has_text() and not message.is_editing()

    def handle(self, message):
        logging.debug("[Chat %s %s message length] %s" %
                      (message.chat_type,
                       message.chat_id,
                       len(message.text)))

        self.__indicate_typing(message)
        self.__learn_new_words(message)
        self.__reply(message)

    def __indicate_typing(self, message):
        if message.should_answer():
            self.bot.send_chat_action(chat_id=message.chat_id, action=ChatAction.TYPING)

    def __learn_new_words(self, message):
        self.data_learner.learn(message)

    def __reply(self, message):
        if not message.should_answer:
            return

        text = self.reply_generator.generate(message)
        if text is None:
            return
        reply_to = None if not message.is_reply_to_bot() else message.message.message_id

        logging.debug("[Chat %s %s answer/reply] %s" %
                      (message.chat_type,
                       message.chat_id,
                       text))

        self.bot.send_message(
            chat_id=message.chat_id,
            reply_to_message_id=reply_to,
            text=text
        )
