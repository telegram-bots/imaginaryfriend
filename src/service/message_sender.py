import logging


class MessageSender:
    def __init__(self, bot):
        self.bot = bot

    def answer(self, entity, message):
        if message == '':
            return

        logging.debug("[Chat %s %s answer] %s" %
                      (entity.chat.chat_type,
                       entity.chat.telegram_id,
                       message))

        self.bot.sendMessage(chat_id=entity.chat.telegram_id, text=message)

    def reply(self, entity, message):
        if message == '':
            return

        logging.debug("[Chat %s %s reply] %s" %
                      (entity.chat.chat_type,
                       entity.chat.telegram_id,
                       message))

        self.bot.sendMessage(chat_id=entity.chat.telegram_id,
                             reply_to_message_id=entity.message.message_id,
                             text=message)

    def send_sticker(self, entity, sticker_id):
        if sticker_id == '':
            return

        logging.debug("[Chat %s %s send_sticker] %s" %
                      (entity.chat.chat_type,
                       entity.chat.telegram_id,
                       sticker_id))

        self.bot.sendSticker(chat_id=entity.chat.telegram_id,
                             reply_to_message_id=entity.message.message_id,
                             sticker=sticker_id)
