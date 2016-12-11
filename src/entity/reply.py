from orator.orm import Model
from orator.orm import belongs_to
from orator.orm import belongs_to_many

import src.entity.pair
import src.entity.word


class Reply(Model):
    """
    Reply entity, represents replies table.
    """
    __fillable__ = ['pair_id', 'word_id', 'count']
    __timestamps__ = False

    @belongs_to_many
    def pairs(self):
        return src.entity.pair.Pair

    @belongs_to
    def word(self):
        return src.entity.word.Word
