from datetime import datetime, timedelta
from orator.orm import Model
from orator.orm import belongs_to
from orator.orm import has_many

from src.utils import random_element
import src.entity.reply
import src.entity.chat
import src.entity.word


class Pair(Model):
    __fillable__ = ['chat_id', 'first_id', 'second_id']
    __timestamps__ = ['created_at']

    @has_many
    def replies(self):
        return src.entity.reply.Reply

    @belongs_to
    def chat(self):
        return src.entity.chat.Chat

    @belongs_to
    def first(self):
        return src.entity.word.Word

    @belongs_to
    def second(self):
        return src.entity.word.Word

    @staticmethod
    def get_random_pair(chat_id, first_id, second_id_list):
        pairs = Pair\
            .with_({
                'replies': lambda q: q.order_by('count', 'desc').limit(3)
            })\
            .where('chat_id', chat_id)\
            .where('first_id', first_id)\
            .where_in('second_id', second_id_list)\
            .limit(3)\
            .get()\
            .all()

        return random_element(pairs)
