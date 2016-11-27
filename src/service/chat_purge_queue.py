import logging

from datetime import datetime, timedelta
from telegram.ext import Job
from src.entity.chat import Chat
from src.entity.reply import Reply
from src.entity.job import Job as JobEntity
from src.config import config


class ChatPurgeQueue:
    queue = None
    jobs = {}
    default_interval = config.getfloat('bot', 'purge_interval')
    job_type = 'purge'

    # TODO. Должно взять все задачи из таблицы и проинициализировать их
    def __init__(self, queue):
        self.queue = queue
        existing_jobs = JobEntity.where('type', self.job_type).get().all()

        for job in existing_jobs:
            current_datetime = datetime.now()
            if current_datetime >= job.execute_at:
                interval = 60
            else:
                interval = (job.execute_at - current_datetime).total_seconds()

            self.add(chat_id=job.chat_id, interval=interval, write_to_db=False)

    def add(self, chat_id, interval=default_interval, write_to_db=True):
        scheduled_at = datetime.now() + timedelta(seconds=interval)

        logging.info("Added chat #%d to purge queue, scheduled to run at %s" %
                     (chat_id, scheduled_at))

        job = self.__make_purge_job(chat_id, interval)
        self.jobs[chat_id] = job
        self.queue.put(job)

        if write_to_db:
            JobEntity.create(chat_id=chat_id,
                             type=self.job_type,
                             repeat=False,
                             execute_at=scheduled_at)

    def remove(self, chat_id):
        if chat_id not in self.jobs:
            return

        logging.info("Removed chat #%d from purge queue" % chat_id)

        job = self.jobs.pop(chat_id)
        job.schedule_removal()
        JobEntity.where('chat_id', chat_id).where('type', self.job_type).delete()

    def __make_purge_job(self, chat_id, interval=default_interval):
        return Job(self.__purge_callback, interval, repeat=False, context=chat_id)

    def __purge_callback(self, bot, job):
        chat_id = job.context
        logging.info("Removing chat #%d data..." % chat_id)

        chat = Chat.find(chat_id)
        if chat is not None:
            for pairs in chat.pairs().select('id').chunk(500):
                Reply.where_in('pair_id', pairs.pluck('id').all()).delete()
            chat.pairs().delete()
            chat.delete()

        JobEntity.where('chat_id', chat_id).where('type', self.job_type).delete()
