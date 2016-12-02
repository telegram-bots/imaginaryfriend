from orator.orm import Model

class Word(Model):
    __fillable__ = ['word']
    __timestamps__ = False
