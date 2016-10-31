from orator.orm import Model
from orator.orm import has_many
from orator.orm import belongs_to
from src.domain.reply import Reply
from src.domain.chat import Chat


class Pair(Model):
    @has_many
    def replies(self):
        return Reply

    @belongs_to
    def chat(self):
        return Chat
