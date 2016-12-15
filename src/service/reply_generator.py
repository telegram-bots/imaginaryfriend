from src.config import config, redis, encoding
from src.utils import strings_has_equal_letters, capitalize, random_element


class ReplyGenerator:
    def __init__(self, tokenizer):
        self.redis = redis
        self.tokenizer = tokenizer
        self.max_words = config.getint('grammar', 'max_words')
        self.max_messages = config.getint('grammar', 'max_messages')

    def generate(self, message):
        messages = []

        words = self.tokenizer.extract_words(message)
        for trigram in self.tokenizer.split_to_trigrams(words):
            pair = trigram[:-1]

            best_message = ''
            for _ in range(self.max_messages):
                generated = self.__generate_sentence(message.chat_id, pair)
                if len(generated) > len(best_message):
                    best_message = generated

            if best_message:
                messages.append(best_message)

        result = random_element(messages) if len(messages) else ''

        if strings_has_equal_letters(result, ''.join(words)):
            return ''

        return result

    def __generate_sentence(self, chat_id, seed):
        key = seed
        gen_words = []
        redis = self.redis.instance()

        for _ in range(self.max_words):
            words = key

            if len(gen_words):
                gen_words.append(words[0])
            else:
                gen_words.append(capitalize(words[0]))

            next_word = redis.srandmember(self.tokenizer.to_key(chat_id=chat_id, pair=key))
            if next_word is None:
                break
            next_word = next_word.decode(encoding)
            if next_word == self.tokenizer.stop_word:
                break

            key = words[1:] + [next_word]

        sentence = ' '.join(gen_words).strip()
        if sentence[-1:] not in self.tokenizer.end_sentence:
            sentence += self.tokenizer.random_end_sentence_token()

        return sentence
