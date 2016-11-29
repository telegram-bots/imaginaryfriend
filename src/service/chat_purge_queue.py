import logging
import json

from datetime import datetime, timedelta
from telegram.ext import Job
from src.entity.chat import Chat
from src.entity.reply import Reply
from src.config import config


class ChatPurgeQueue:
    jobs = {}
    default_interval = config.getfloat('bot', 'purge_interval')

    def __init__(self, queue, redis):
        self.queue = queue
        self.redis = redis
        existing_jobs = map(lambda j: json.loads(j.decode('utf-8')),
                            redis.instance().hgetall('purge_queue').values())

        for job in existing_jobs:
            job_datetime = datetime.fromtimestamp(job['execute_at'])
            current_datetime = datetime.now()

            if current_datetime >= job_datetime:
                interval = 60
            else:
                interval = (job_datetime - current_datetime).total_seconds()

            self.add(chat_id=job['chat_id'], interval=interval, write_to_db=False)

    def add(self, chat_id, interval=default_interval, write_to_db=True):
        scheduled_at = datetime.now() + timedelta(seconds=interval)

        logging.info("Added chat #%d to purge queue, scheduled to run at %s" %
                     (chat_id, scheduled_at))

        job = self.__make_purge_job(chat_id, interval)
        self.jobs[chat_id] = job
        self.queue.put(job)

        if write_to_db:
            self.redis.instance().hset(
                "purge_queue",
                chat_id,
                json.dumps({'chat_id': chat_id, 'execute_at': scheduled_at.timestamp()}))

    def remove(self, chat_id):
        if chat_id not in self.jobs:
            return

        logging.info("Removed chat #%d from purge queue" % chat_id)

        job = self.jobs.pop(chat_id)
        job.schedule_removal()
        self.redis.instance().hdel("purge_queue", chat_id)

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

        self.redis.instance().hdel("purge_queue", chat_id)
