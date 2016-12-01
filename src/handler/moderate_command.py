from src.entity.pair import Pair
from src.entity.reply import Reply
from src.entity.word import Word


class ModerateCommand:
    def __init__(self, bot, entity):
        self.bot = bot
        self.entity = entity

    def __formatted_view(self, words):
        list = []
        for k, v in words.items():
            list.append("- %s : %d" % (v, k))

        return '\n'.join(list)

    def __find_pairs(self, chat_id, word_ids):
        return Pair.where('chat_id', chat_id) \
            .where(
                Pair.query().where_in('first_id', word_ids)
                    .or_where_in('second_id', word_ids)
            ) \
            .get()

    def __find_current_chat_words(self, search_word):
        found_words = Word.where('word', 'like', search_word + '%') \
            .order_by('word', 'asc') \
            .limit(10) \
            .lists('word', 'id')

        if len(found_words) == 0:
            return []

        to_keep = []
        for pair in self.__find_pairs(self.entity.chat_id, list(found_words.keys())):
            if pair.first_id in found_words:
                to_keep.append(pair.first_id)
            if pair.second_id in found_words:
                to_keep.append(pair.second_id)

        to_keep = set(to_keep)

        return dict((k, found_words[k]) for k in found_words if k in to_keep)

    def is_admin(self):
        user_id = self.entity.message.from_user.id
        admin_ids = list(map(
            lambda member: member.user.id,
            self.bot.get_chat_administrators(chat_id=self.entity.chat_id)
        ))

        return user_id in admin_ids

    def remove_word(self, word_id):
        pairs_ids = self.__find_pairs(self.entity.chat_id, [word_id]).lists('id')

        Pair.where_in('id', pairs_ids).delete()
        Reply.where_in('pair_id', pairs_ids).delete()

    def find_similar_words(self, word):
        found_words = self.__find_current_chat_words(word)

        if len(found_words) == 0:
            return 'No words found!'

        return self.__formatted_view(found_words)
