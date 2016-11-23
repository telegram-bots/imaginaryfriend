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

        self.bot.send_message(chat_id=entity.chat.telegram_id, text=message)

    def reply(self, entity, message):
        if message == '':
            return

        logging.debug("[Chat %s %s reply] %s" %
                      (entity.chat.chat_type,
                       entity.chat.telegram_id,
                       message))

        self.bot.send_message(chat_id=entity.chat.telegram_id,
                              reply_to_message_id=entity.message.message_id,
                              text=message)

    def send_reply_markup(self, entity, message, reply_markup):
        self.bot.send_message(chat_id=entity.chat.telegram_id,
                              text=message,
                              reply_markup=reply_markup)

    def send_action(self, entity, action):
        logging.debug("[Chat %s %s send_action] %s" %
                      (entity.chat.chat_type,
                       entity.chat.telegram_id,
                       action))

        self.bot.send_chat_action(chat_id=entity.chat.telegram_id, action=action)

    def send_sticker(self, entity, sticker_id):
        if sticker_id == '':
            return

        logging.debug("[Chat %s %s send_sticker] %s" %
                      (entity.chat.chat_type,
                       entity.chat.telegram_id,
                       sticker_id))

        self.bot.send_sticker(chat_id=entity.chat.telegram_id,
                              reply_to_message_id=entity.message.message_id,
                              sticker=sticker_id)
