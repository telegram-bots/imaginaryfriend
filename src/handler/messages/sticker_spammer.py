import logging
from .base import Base
from random import choice
from src.component.config import config


class StickerSpammer(Base):
    def __init__(self):
        super().__init__()
        self.stickers = config.getlist('bot', 'spam_stickers')

    def can_handle(self, message):
        return message.is_sticker() \
               and (message.has_anchors() or message.is_private() or message.is_reply_to_bot())

    def handle(self, message):
        logging.debug("[Chat %s %s spam_sticker]" %
                      (message.chat_type,
                       message.chat_id))

        self.bot.send_sticker(
            chat_id=message.chat_id,
            reply_to_message_id=message.message.message_id,
            sticker=choice(self.stickers)
        )

