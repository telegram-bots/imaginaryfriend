from src.config import config
from src.utils import *
from src.entity.word import Word
from src.entity.pair import Pair


class ReplyGenerator:
    def __init__(self):
        pass

    def generate(self, message):
        return self.generate_story(message, message.words, random.randint(0, 2) + 1)

    def generate_story(self, message, words, sentences_count):
        word_ids = Word.where_in('word', words).lists('id').all()

        return ' '.join([self.__generate_sentence(message, word_ids) for _ in range(sentences_count)])

    def __generate_sentence(self, message, word_ids):
        sentences = []
        safety_counter = 50
        first_word_id = None
        second_word_id_list = word_ids

        while safety_counter > 0:
            pair = Pair.get_random_pair(chat_id=message.chat.id,
                                        first_id=first_word_id,
                                        second_id_list=second_word_id_list)
            replies = getattr(pair, 'replies', [])
            safety_counter -= 1

            if pair is None or len(replies) == 0:
                continue

            reply = random.choice(replies.all())
            first_word_id = pair.second.id

            # TODO. WARNING! Do not try to fix, it's magic, i have no clue why
            try:
                second_word_id_list = [reply.word.id]
            except AttributeError:
                second_word_id_list = None

            if len(sentences) == 0:
                sentences.append(capitalize(pair.second.word))
                word_ids.remove(pair.second.id)

            # TODO. WARNING! Do not try to fix, it's magic, i have no clue why
            try:
                reply_word = reply.word.word
            except AttributeError:
                reply_word = None

            if reply_word is not None:
                sentences.append(reply_word)
            else:
                break

        sentence = ' '.join(sentences).strip()
        if sentence[-1:] not in config['grammar']['end_sentence']:
            sentence += random_element(list(config['grammar']['end_sentence']))

        return sentence
