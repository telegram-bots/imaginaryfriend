from src.entity.pair import Pair
from src.entity.reply import Reply
from src.entity.word import Word
from src.utils import safe_cast
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

            if safe_cast(command.args[0], int) is None:
                Moderate.reply(bot, command, Moderate.find_similar_words(command.chat_id, command.args[0]))
            else:
                Moderate.remove_word(command.chat_id, int(command.args[0]))
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

    @staticmethod
    def remove_word(chat_id, word_id):
        pairs_ids = Moderate.__find_pairs(chat_id, [word_id]).lists('id')

        Pair.where_in('id', pairs_ids).delete()
        Reply.where_in('pair_id', pairs_ids).delete()

    @staticmethod
    def find_similar_words(chat_id, word):
        found_words = Moderate.__find_chat_words(chat_id, word)

        if len(found_words) == 0:
            return 'No words found!'

        return Moderate.__formatted_view(found_words)

    @staticmethod
    def __formatted_view(words):
        result = []
        for k, v in words.items():
            result.append("%s : %d" % (v, k))

        return '\n'.join(result)

    @staticmethod
    def __find_pairs(chat_id, word_ids):
        return Pair.where('chat_id', chat_id) \
            .where(
                Pair.query().where_in('first_id', word_ids)
                    .or_where_in('second_id', word_ids)
            ) \
            .get()

    @staticmethod
    def __prepare_word(word):
        return word.strip("'\"")

    @staticmethod
    def __find_chat_words(chat_id, search_word):
        found_words = Word.where('word', 'like', Moderate.__prepare_word(search_word) + '%') \
            .order_by('word', 'asc') \
            .limit(10) \
            .lists('word', 'id')

        if len(found_words) == 0:
            return []

        to_keep = []
        for pair in Moderate.__find_pairs(chat_id, list(found_words.keys())):
            if pair.first_id in found_words:
                to_keep.append(pair.first_id)
            if pair.second_id in found_words:
                to_keep.append(pair.second_id)

        to_keep = set(to_keep)

        return dict((k, found_words[k]) for k in found_words if k in to_keep)
