from orator.orm import Model


class Word(Model):
    """
    Word entity, represents words table.
    """
    __fillable__ = ['word']
    __timestamps__ = False
