from .base import Base
from src.component.config import config, trigram_repository


class Moderate(Base):
    aliases = ['mod_f', 'mod_d']
    gods = config.getlist('bot', 'god_mode', type=int)

    def execute(self, command):
        try:
            if not command.is_private() and not self.__is_admin(command):
                return self.reply(command, 'You don\'t have admin privileges!')

            if len(command.args) == 0:
                raise IndexError

            if command.name == 'mod_f':
                words = trigram_repository.find_word(command.chat_id, command.args[0].strip())
                reply = '\n'.join(words)
                if reply.strip() == '':
                    reply = 'Nothing found'

                self.reply(command, reply)
            elif command.name == 'mod_d':
                trigram_repository.remove_word(command.chat_id, command.args[0].strip())
        except (IndexError, ValueError):
            self.reply(command, """Usage:
/mod_f <similar_word> for search
/mod_d <exact_word> for deletion""")

    def __is_admin(self, entity):
        user_id = entity.message.from_user.id
        admin_ids = list(map(lambda m: m.user.id, self.bot.get_chat_administrators(entity.chat_id)))

        return user_id in admin_ids \
               or user_id in self.gods
