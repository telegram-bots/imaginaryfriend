import logging.config
from orator.orm import Model
from orator import DatabaseManager
from src.config import config, redis
from src.entity.pair import Pair


def main():
    logging.basicConfig(level='DEBUG')
    Model.set_connection_resolver(DatabaseManager({'db': config['db']}))

    redis_c = redis.instance()
    counter = 0
    key = 'trigrams:{}:{}'
    for pairs in Pair.with_('replies', 'first', 'second').chunk(500):
        for pair in pairs:
            try:
                first = clear_word(pair.first.word)
            except AttributeError:
                first = config['grammar']['stop_word']

            try:
                second = clear_word(pair.second.word)
            except AttributeError:
                second = config['grammar']['stop_word']

            point = to_key(key=key, chat_id=pair.chat_id, pair=[first, second])
            replies = list(filter(None, map(get_word, pair.replies.all())))

            if len(replies) == 0:
                continue

            pipe = redis_c.pipeline()
            for reply in replies:
                pipe.sadd(point, reply)
            pipe.execute()

            counter += 1

            if counter % 1000 == 0:
                print("Imported: " + str(counter))

def clear_word(word):
    return word.strip(";()\-—\"[]{}«»/*&^#$")

def get_word(reply):
    try:
        return clear_word(reply.word.word)
    except AttributeError:
        return None

def to_key(key, chat_id, pair):
    return key.format(chat_id, config['grammar']['separator'].join(pair))

if __name__ == '__main__':
    main()
