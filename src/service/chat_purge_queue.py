import logging

from datetime import datetime, timedelta
from telegram.ext import Job
from src.component.config import config, trigram_repository, job_repository


class ChatPurgeQueue:
    """
    Scheduling and execution of chat purge
    """
    def __init__(self):
        self.queue = None
        self.jobs = {}
        self.job_repository = job_repository
        self.trigram_repository = trigram_repository
        self.default_interval = config.getfloat('bot', 'purge_interval')

    def instance(self, queue):
        self.queue = queue

        self.__load_existing_jobs()

        return self

    def add(self, chat_id, interval=None, db=True):
        """
        Schedules purge of chat data
        :param chat_id: ID of chat
        :param interval: Interval in seconds
        :param db: Should be added to db or not
        """
        interval = interval if interval is not None else self.default_interval
        scheduled_at = datetime.now() + timedelta(seconds=interval)

        logging.info("Added chat #%d to purge queue, scheduled to run at %s" %
                     (chat_id, scheduled_at))

        job = self.__make_purge_job(chat_id, interval)
        self.jobs[chat_id] = job
        self.queue.put(job)

        if db is True:
            self.job_repository.add(chat_id, scheduled_at)

    def remove(self, chat_id):
        """
        Removes scheduled purge job from queue
        :param chat_id: ID of chat
        """
        if chat_id not in self.jobs:
            return

        logging.info("Removed chat #%d from purge queue" % chat_id)

        job = self.jobs.pop(chat_id)
        job.schedule_removal()

        self.job_repository.delete(chat_id)

    def __load_existing_jobs(self):
        existing_jobs = self.job_repository.get_all()

        for job in existing_jobs:
            interval = self.__timestamp_to_interval(job['execute_at'])
            self.add(chat_id=job['chat_id'], interval=interval, db=False)

    def __timestamp_to_interval(self, timestamp):
        date_time = datetime.fromtimestamp(timestamp)
        current_datetime = datetime.now()

        if current_datetime >= date_time:
            interval = 60
        else:
            interval = (date_time - current_datetime).total_seconds()

        return interval

    def __make_purge_job(self, chat_id, interval):
        return Job(self.__purge_callback, interval, repeat=False, context=chat_id)

    def __purge_callback(self, bot, job):
        chat_id = job.context

        logging.info("Removing chat #%d data..." % chat_id)

        self.trigram_repository.clear(chat_id)
        self.job_repository.delete(chat_id)
