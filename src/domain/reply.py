from orator.orm import Model
from orator.orm import belongs_to
from orator.orm import belongs_to_many

import src.domain.pair
import src.domain.word


class Reply(Model):
    __guarded__ = ['id']
    __timestamps__ = False

    @belongs_to_many
    def pairs(self):
        return src.domain.pair.Pair

    @belongs_to
    def word(self):
        return src.domain.word.Word
