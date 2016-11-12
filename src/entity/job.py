from orator.orm import Model
from orator.orm import belongs_to

import src.entity.chat


class Job(Model):
    __fillable__ = ['chat_id', 'type', 'repeat', 'execute_at']
    __timestamps__ = False
    __dates__ = ['execute_at']

    @belongs_to
    def chat(self):
        return src.entity.chat.Chat
