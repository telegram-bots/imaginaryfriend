import logging

from telegram.ext import MessageHandler, Filters

from src.domain.status import Status
from src.entity.chat import Chat
from src import chat_purge_queue


class StatusHandler(MessageHandler):
    def __init__(self, config):
        super(StatusHandler, self).__init__(
            Filters.status_update,
            self.handle,
            pass_job_queue=True)

        self.config = config

    def handle(self, bot, update, job_queue):
        chat = Chat.get_chat(update.message)
        status = Status(chat=chat, message=update.message, config=self.config)

        if status.is_bot_added():
            return self.__process_bot_add(status, job_queue)
        elif status.is_bot_kicked():
            return self.__process_bot_kick(status, job_queue)

    def __process_bot_kick(self, status, job_queue):
        logging.debug("[Chat %s %s bot_kicked]" %
                      (status.chat.chat_type, status.chat.telegram_id))

        chat_purge_queue.add(status.chat.id)

    def __process_bot_add(self, status, job_queue):
        logging.debug("[Chat %s %s bot_added]" %
                      (status.chat.chat_type, status.chat.telegram_id))

        chat_purge_queue.remove(status.chat.id)
