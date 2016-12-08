import logging
from abc import ABC, abstractmethod


class Base(ABC):
    name = None
    aliases = []

    @staticmethod
    @abstractmethod
    def execute(bot, command):
        pass

    @staticmethod
    def reply(bot, command, message):
        logging.debug("[Chat %s %s command] %s: %s" %
                      (command.chat_type,
                       command.chat_id,
                       command.name,
                       message))

        bot.send_message(chat_id=command.chat_id,
                         reply_to_message_id=command.message.message_id,
                         text=message)
