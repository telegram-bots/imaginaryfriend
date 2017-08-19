import logging
from .base import Base
from random import choice
from src.component.config import config, media_checker


class MediaChecker(Base):
    def __init__(self):
        super().__init__()
        self.media_checker = media_checker
        self.messages = config.getlist('media_checker', 'messages')

    def can_handle(self, message):
        return message.has_text() \
               and not message.is_editing() \
               and not message.is_private() \
               and message.has_entities()

    def handle(self, message):
        if self.media_checker.check(message):
            logging.debug("[Chat %s %s not unique media]" %
                          (message.chat_type,
                           message.chat_id))

            self.bot.send_message(
                chat_id=message.chat_id,
                reply_to_message_id=message.message.message_id,
                text=choice(self.messages)
            )
