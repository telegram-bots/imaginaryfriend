from .base import Base
from src.config import config, trigram_repository


class Moderate(Base):
    aliases = ['mod_f', 'mod_d']
    gods = [int(id) for id in config.getlist('bot', 'god_mode')]

    @staticmethod
    def execute(bot, command):
        try:
            if not command.is_private() and not Moderate.is_admin(bot, command):
                return Moderate.reply(bot, command, 'You don\'t have admin privileges!')

            if len(command.args) == 0:
                raise IndexError

            if command.name == 'mod_f':
                words = trigram_repository.find_word(command.chat_id, command.args[0].strip())
                reply = '\n'.join(words)
                if reply == '':
                    reply = 'Nothing found'

                Moderate.reply(bot, command, reply)
            elif command.name == 'mod_d':
                trigram_repository.remove_word(command.chat_id, command.args[0].strip())
        except (IndexError, ValueError):
            Moderate.reply(bot, command, """Usage:
/mod_f <similar_word> for search
/mod_d <exact_word> for deletion""")

    @staticmethod
    def is_admin(bot, entity):
        user_id = entity.message.from_user.id
        admin_ids = list(map(lambda m: m.user.id, bot.get_chat_administrators(entity.chat_id)))

        return user_id in admin_ids or user_id in Moderate.gods
