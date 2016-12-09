import re
from src.utils import random_element
from src.config import config


class Tokenizer:
    def __init__(self):
        self.key = 'trigrams:{}:{}'
        self.chain_length = config.getint('grammar', 'chain_length')
        self.separator = config['grammar']['separator']
        self.stop_word = config['grammar']['stop_word']
        self.end_sentence = config['grammar']['end_sentence']
        self.garbage_tokens = config['grammar']['all']

    def split_to_trigrams(self, words):
        if len(words) <= self.chain_length:
            yield from ()

        words.append(self.stop_word)
        for i in range(len(words) - self.chain_length):
            yield words[i:i + self.chain_length + 1]

    def extract_words(self, message):
        symbols = list(re.sub('\s', ' ', message.text))

        for entity in message.entities:
            symbols[entity.offset:entity.length + entity.offset] = ' ' * entity.length

        return list(filter(None, map(self.__prettify, ''.join(symbols).split(' '))))

    def to_key(self, chat_id, pair):
        return self.key.format(chat_id, self.separator.join(pair))

    def random_end_sentence_token(self):
        return random_element(list(self.end_sentence))

    def __prettify(self, word):
        lowercase_word = word.lower().strip()
        last_symbol = lowercase_word[-1:]
        if last_symbol not in self.end_sentence:
            last_symbol = ''
        pretty_word = lowercase_word.strip(self.garbage_tokens)

        if pretty_word != '' and len(pretty_word) > 2:
            return pretty_word + last_symbol
        elif lowercase_word in self.garbage_tokens:
            return None

        return lowercase_word
