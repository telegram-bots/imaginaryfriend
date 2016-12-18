# Config
import configparser

encoding = 'utf-8'

sections = {
    'bot': ['token', 'name', 'anchors', 'messages', 'purge_interval', 'default_chance', 'spam_stickers'],
    'grammar': ['chain_length', 'separator', 'stop_word', 'end_sentence', 'all'],
    'logging': ['level'],
    'updates': ['mode'],
    'media_checker': ['lifetime', 'stickers'],
    'redis': ['host', 'port', 'db'],
    'db': []
}


def getlist(self, section, option, type=str):
    return list(map(lambda o: type(o), config.get(section, option).split(',')))

configparser.ConfigParser.getlist = getlist

config = configparser.ConfigParser()
config.read('./main.cfg', encoding=encoding)

for section, options in sections.items():
    if not config.has_section(section):
        raise ValueError("Config is not valid! Section '{}' is missing!".format(section))
    for option in options:
        if not config.has_option(section, option):
            raise ValueError("Config is not valid! Option '{}' in section '{}' is missing!".format(option, section))


# IOC
from src.redis_c import Redis
redis = Redis(config)

from src.service.tokenizer import Tokenizer
tokenz = Tokenizer()

from src.repository import *
trigram_repository = TrigramRepository()
chance_repository = ChanceRepository()
media_repository = MediaRepository()
job_repository = JobRepository()

from src.service import *
data_learner = DataLearner(tokenz)
reply_generator = ReplyGenerator(tokenz)
media_checker = MediaUniquenessChecker()
chat_purge_queue = ChatPurgeQueue()
