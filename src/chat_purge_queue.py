import logging

from telegram.ext import Job
from src.entity.chat import Chat
from src import config


class ChatPurgeQueue:
    queue = None
    jobs = {}
    default_interval = float(config['bot']['default_interval'])

    # TODO. Должно взять все задачи из таблицы и проинициализировать их
    def __init__(self, queue):
        self.queue = queue

    def add(self, chat_id, interval=default_interval):
        if self.queue is None:
            logging.error("Queue is not set!")
            return

        logging.info("Added chat #%d to purge queue, with interval %d" %
                     (chat_id, interval))

        job = self.__make_purge_job(chat_id, interval)
        self.jobs[chat_id] = job
        self.queue.put(job)

    def remove(self, chat_id):
        if self.queue is None:
            logging.error("Queue is not set!")
            return
        if chat_id not in self.jobs:
            return

        logging.info("Removed chat #%d from purge queue" % chat_id)

        job = self.jobs.pop(chat_id)
        job.schedule_removal()

    def __make_purge_job(self, chat_id, interval=default_interval):
        return Job(self.__purge_callback, interval, repeat=False, context=chat_id)

    def __purge_callback(self, bot, job):
        chat_id = job.context
        logging.info("Removing chat #%d data..." % chat_id)

        chat = Chat.find(chat_id)
        if chat is not None:
            chat.pairs().delete()
            chat.delete()
