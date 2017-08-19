import re
from random import choice
from src.component.config import config


class Tokenizer:
    def __init__(self):
        self.chain_len = config.getint('grammar', 'chain_len')
        self.stop_word = config['grammar']['stop_word']
        self.endsen   = config['grammar']['endsen']
        self.garbage   = config['grammar']['garbage']
        # https://core.telegram.org/bots/api#messageentity
        self.garbage_entities = config.getlist('grammar', 'garbage_entities')

    def split_to_trigrams(self, words_list):
        if len(words_list) <= self.chain_len:
            yield from ()

        words = [self.stop_word]

        for word in words_list:
            words.append(word)
            if word[-1] in self.endsen:
                words.append(self.stop_word)
        if words[-1] != self.stop_word:
            words.append(self.stop_word)

        for i in range(len(words) - self.chain_len):
            j = i + self.chain_len + 1 
            yield words[i:j]

    def extract_words(self, message):
        symbols = list(re.sub('\s', ' ', self.remove_garbage_entities(message)))

        return list(filter(None, map(self.prettify, ''.join(symbols).split(' '))))

    def random_end_sentence_token(self):
        return choice(list(self.endsen))

    def remove_garbage_entities(self, message):
        encoding = 'utf-16-le'
        utf16bytes = message.text.encode(encoding)
        result = bytearray()
        cur_pos = 0

        for e in message.entities:
            start_pos = e.offset * 2
            end_pos = (e.offset + e.length) * 2

            result += utf16bytes[cur_pos:start_pos]
            if e.type not in self.garbage_entities:
                result += utf16bytes[start_pos:end_pos]

            cur_pos = end_pos

        result += utf16bytes[cur_pos:]

        return utf16bytes.decode(encoding)

    def prettify(self, word):
        lowercase_word = word.lower().strip()
        last_symbol = lowercase_word[-1:]
        if last_symbol not in self.endsen:
            last_symbol = ''
        pretty_word = lowercase_word.strip(self.garbage)

        if pretty_word != '' and len(pretty_word) > 2:
            return pretty_word + last_symbol
        elif lowercase_word in self.garbage:
            return None

        return lowercase_word
