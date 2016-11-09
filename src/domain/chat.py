from orator.orm import Model
from orator.orm import has_many
import logging

import src.domain.pair


class Chat(Model):
    __guarded__ = ['id']

    @has_many
    def pairs(self):
        return src.domain.pair.Pair

    # def migrate_to_chat_id(self, new_id):
    #     logging.info("[Chat %s %s] Migrating ID to %s" % (self.chat_type, self.telegram_id, new_id))
    #     self.telegram_id = new_id
    #     self.save()

    @staticmethod
    def get_chat(message):
        telegram_id = message.chat.id
        type = message.chat.type

        return Chat.first_or_create(telegram_id=telegram_id, chat_type=type)

# Events
Chat.created(lambda chat: logging.info("[Chat %s %s] Created with internal ID #%s" %
                                   (chat.chat_type, chat.telegram_id, chat.id)))

#TODO Fix
#Chat.updating(lambda chat: logging.info("[Chat %s %s New gab level is set to %s" %
#                                   (chat.chat_type, chat.telegram_id, chat.random_chance)))