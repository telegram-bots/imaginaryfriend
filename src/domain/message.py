from orator import Model


class Message(Model):
    __fillable__ = ['chat_id', 'user_name', 'user_id', 'payload']
    __guarded__ = ['id']
