import logging
import json

from datetime import datetime, timedelta
from telegram.ext import Job
from src.entity.reply import Reply
from src.entity.pair import Pair
from src.config import config


class ChatPurgeQueue:
    jobs = {}
    default_interval = config.getfloat('bot', 'purge_interval')
    key = 'purge_queue'

    def __init__(self, queue, redis):
        self.queue = queue
        self.redis = redis

        self.__load_existing_jobs()

    def add(self, chat_id, interval=default_interval):
        scheduled_at = datetime.now() + timedelta(seconds=interval)

        logging.info("Added chat #%d to purge queue, scheduled to run at %s" %
                     (chat_id, scheduled_at))

        job = self.__make_purge_job(chat_id, interval)
        self.jobs[chat_id] = job
        self.queue.put(job)

        self.redis.instance().hset(
            self.key,
            chat_id,
            json.dumps({'chat_id': chat_id, 'execute_at': scheduled_at.timestamp()})
        )

    def remove(self, chat_id):
        if chat_id not in self.jobs:
            return

        logging.info("Removed chat #%d from purge queue" % chat_id)

        job = self.jobs.pop(chat_id)
        job.schedule_removal()

        self.redis.instance().hdel(self.key, chat_id)

    def __load_existing_jobs(self):
        existing_jobs = map(lambda j: json.loads(j.decode('utf-8')),
                            self.redis.instance().hgetall(self.key).values())

        for job in existing_jobs:
            job_datetime = datetime.fromtimestamp(job['execute_at'])
            current_datetime = datetime.now()

            if current_datetime >= job_datetime:
                interval = 60
            else:
                interval = (job_datetime - current_datetime).total_seconds()

            self.add(chat_id=job['chat_id'], interval=interval)

    def __make_purge_job(self, chat_id, interval=default_interval):
        return Job(self.__purge_callback, interval, repeat=False, context=chat_id)

    def __purge_callback(self, bot, job):
        chat_id = job.context

        logging.info("Removing chat #%d data..." % chat_id)

        for pairs in Pair.where('chat_id', chat_id).select('id').chunk(500):
            Reply.where_in('pair_id', pairs.pluck('id').all()).delete()
        Pair.where('chat_id', chat_id).delete()

        self.redis.instance().hdel(self.key, chat_id)
