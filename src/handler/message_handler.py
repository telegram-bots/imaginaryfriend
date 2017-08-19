from src.component.config import chance_repository
from telegram.ext import MessageHandler as ParentHandler, Filters
from telegram.ext.dispatcher import run_async
from src.domain.message import Message
from .messages import message_handlers


class MessageHandler(ParentHandler):
    def __init__(self):
        super(MessageHandler, self).__init__(
            Filters.text | Filters.sticker | Filters.photo,
            self.handle
        )
        self.chance_repository = chance_repository
        self.handlers = message_handlers

    @run_async
    def handle(self, bot, update):
        chance = self.chance_repository.get(update.message.chat.id)
        message = Message(chance=chance, message=update.message)

        for handler in message_handlers:
            if handler.bot is None:
                handler.bot = bot
            if handler.can_handle(message):
                handler.handle(message)
