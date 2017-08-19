# Config
import logging
import logging.config
import os.path
from configparser import ConfigParser

import os


def load(file_name):
    app_config = ConfigParser()
    app_config.read(os.path.join('resources', 'cfg', file_name), encoding=encoding)

    user_app_config = os.getenv('CONFIG_PATH', os.path.join('cfg', file_name))
    if os.path.exists(user_app_config) and os.path.isfile(user_app_config):
        app_config.read(user_app_config, encoding=encoding)

    return app_config


def extend(conf):
    def getlist(self, section, option, type=str):
        return list(map(lambda o: type(o), conf.get(section, option).split(',')))

    ConfigParser.getlist = getlist

    return conf


def validate(conf, sections):
    for section, options in sections.items():
        if not conf.has_section(section):
            raise ValueError("Config is not valid!",
                             "Section '{}' is missing!".format(section))
        for option in options:
            if not conf.has_option(section, option):
                raise ValueError("Config is not valid!",
                                 "Option '{}' in section '{}' is missing!".format(option, section))

    return conf


def setup_logging(file_name):
    log_config = ConfigParser()
    log_config.read(os.path.join('resources', 'cfg', file_name), encoding=encoding)

    user_log_config = os.getenv('LOGGING_CONFIG_PATH', os.path.join('cfg', file_name))
    if os.path.exists(user_log_config) and os.path.isfile(user_log_config):
        log_config.read(user_log_config, encoding=encoding)

    logging.config.fileConfig(log_config)

encoding = 'utf-8'
setup_logging('logging.conf')
config = validate(extend(load('app.conf')), sections={
    'bot': ['token', 'name', 'anchors', 'god_mode', 'purge_interval', 'default_chance', 'spam_stickers'],
    'grammar': ['chain_len', 'sep', 'stop_word', 'max_wrds', 'max_msgs', 'endsen', 'garbage', 'garbage_entities'],
    'logging': ['level'],
    'updates': ['mode'],
    'media_checker': ['lifetime', 'messages'],
    'redis': ['host', 'port', 'db']
})

# IOC
from src.component.redis_c import Redis
redis = Redis(config)

from src.component.tokenizer import Tokenizer
tokenizer = Tokenizer()

from src.repository import *
trigram_repository = TrigramRepository()
chance_repository = ChanceRepository()
media_repository = MediaRepository()
job_repository = JobRepository()

from src.service import *
data_learner = DataLearner()
reply_generator = ReplyGenerator()
media_checker = MediaUniquenessChecker()
chat_purge_queue = ChatPurgeQueue()
