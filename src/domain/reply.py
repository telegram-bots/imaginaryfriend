from orator.orm import Model
from orator.orm import belongs_to
from orator.orm import belongs_to_many

from . import (Pair, Word)


class Reply(Model):
    __guarded__ = ['id']

    @belongs_to_many
    def pairs(self):
        return Pair

    @belongs_to
    def word(self):
        return Word
