from src.config import config, redis, tokenz, trigram_repository
from src.utils import strings_has_equal_letters, capitalize


class ReplyGenerator:
    def __init__(self):
        self.redis = redis
        self.tokenizer = tokenz
        self.trigram_repository = trigram_repository

        self.max_words = config.getint('grammar', 'max_words')
        self.max_messages = config.getint('grammar', 'max_messages')

        self.stop_word = config['grammar']['stop_word']
        self.separator = config['grammar']['separator']
        self.end_sentence = config['grammar']['end_sentence']

    def generate(self, message):
        messages = []

        words = self.tokenizer.extract_words(message)
        for trigram in self.tokenizer.split_to_trigrams(words):
            pair = trigram[:-1]

            messages.append(self.__generate_best_message(chat_id=message.chat_id, pair=pair))

        result = max(messages, key=len) if len(messages) else ''

        if strings_has_equal_letters(result, ''.join(words)):
            return ''

        return result

    def __generate_best_message(self, chat_id, pair):
        best_message = ''
        for _ in range(self.max_messages):
            generated = self.__generate_sentence(chat_id=chat_id, pair=pair)
            if len(generated) > len(best_message):
                best_message = generated

        return best_message

    def __generate_sentence(self, chat_id, pair):
        gen_words = []
        key = self.separator.join(pair)

        for _ in range(self.max_words):
            words = key.split(self.separator)

            gen_words.append(words[0])

            next_word = self.trigram_repository.get_random_reply(chat_id, key)
            if next_word is None:
                break

            key = self.separator.join(words[1:] + [next_word])

        gen_words = list(filter(lambda w: w != self.stop_word, gen_words))
        sentence = ' '.join(gen_words).strip()
        if sentence[-1:] not in self.end_sentence:
            sentence += self.tokenizer.random_end_sentence_token()

        return capitalize(sentence)
