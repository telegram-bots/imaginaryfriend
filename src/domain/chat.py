from orator.orm import Model
from orator.orm import has_many
from src.domain.pair import Pair


class Chat(Model):
    @has_many
    def pairs(self):
        return Pair
