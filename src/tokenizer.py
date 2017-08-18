import re
from src.utils import random_element
from src.config import config


class Tokenizer:
    def __init__(self):
        self.chain_len = config.getint('grammar', 'chain_len')
        self.stop_word = config['grammar']['stop_word']
        self.endsent   = config['grammar']['endsent']
        self.garbage   = config['grammar']['garbage']

    def split_to_trigrams(self, src_words):
        if len(src_words) <= self.chain_len:
            yield from ()

        words = [self.stop_word]

        for word in src_words:
            words.append(word)
            if word[-1] in self.endsent:
                words.append(self.stop_word)
        if words[-1] != self.stop_word:
            words.append(self.stop_word)

        for i in range(len(words) - self.chain_len):
            j = i + self.chain_len + 1 
            yield words[i : j]

    def extract_words(self, message):
        symbols = list(re.sub('\s', ' ', message.text))

        for entity in message.entities:
            # TODO: explain the code
            # TODO: validate the formula
            symbols[entity.offset : (entity.length+entity.offset)] = ' ' * entity.length

        return list(filter(None, map(self.__prettify, ''.join(symbols).split(' '))))

    def random_end_sentence_token(self):
        return random_element(list(self.endsent))

    def __prettify(self, word):
        lowercase_word = word.lower().strip()
        last_symbol = lowercase_word[-1:]
        if last_symbol not in self.endsent:
            last_symbol = ''
        pretty_word = lowercase_word.strip(self.garbage_tokens)

        if pretty_word != '' and len(pretty_word) > 2:
            return pretty_word + last_symbol
        elif lowercase_word in self.garbage_tokens:
            return None

        return lowercase_word
