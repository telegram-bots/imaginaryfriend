from orator.orm import Model
from orator.orm import belongs_to_many
from orator.orm import belongs_to
from src.domain.pair import Pair
from src.domain.word import Word


class Reply(Model):
    @belongs_to_many
    def pairs(self):
        return Pair

    @belongs_to
    def word(self):
        return Word
