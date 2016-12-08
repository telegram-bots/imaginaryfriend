import logging

from telegram.ext import MessageHandler, Filters

from src.domain.status import Status


class StatusHandler(MessageHandler):
    def __init__(self, chat_purge_queue):
        super(StatusHandler, self).__init__(
            Filters.status_update,
            self.handle)

        self.chat_purge_queue = chat_purge_queue

    def handle(self, bot, update):
        status = Status(message=update.message)

        if status.is_bot_added():
            return self.__process_bot_add(status)
        elif status.is_bot_kicked():
            return self.__process_bot_kick(status)

    def __process_bot_kick(self, status):
        logging.debug("[Chat %s %s bot_kicked]" %
                      (status.chat_type, status.chat_id))

        self.chat_purge_queue.add(status.chat_id)

    def __process_bot_add(self, status):
        logging.debug("[Chat %s %s bot_added]" %
                      (status.chat_type, status.chat_id))

        self.chat_purge_queue.remove(status.chat_id)
