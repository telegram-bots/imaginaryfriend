from .base import Base


class Moderate(Base):
    name = 'moderate'

    @staticmethod
    def execute(bot, command):
        try:
            if not command.is_private() and not Moderate.is_admin(bot, command):
                return Moderate.reply(bot, command, 'You don\'t have admin privileges!')

            if len(command.args) == 0:
                raise IndexError

            Moderate.reply(bot, command, 'Command currently disabled.')

            # if safe_cast(command.args[0], int) is None:
            # Moderate.reply(bot, command, Moderate.find_similar_words(command.chat_id, command.args[0]))
            # else:
            # Moderate.remove_word(command.chat_id, int(command.args[0]))
        except (IndexError, ValueError):
            Moderate.reply(bot, command, """Usage:
/moderate <word> for search
/moderate <word_id> for deletion""")

    @staticmethod
    def is_admin(bot, entity):
        user_id = entity.message.from_user.id
        admin_ids = list(map(
            lambda member: member.user.id,
            bot.get_chat_administrators(chat_id=entity.chat_id)
        ))

        return user_id in admin_ids
