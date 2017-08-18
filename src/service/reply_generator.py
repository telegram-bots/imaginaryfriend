from src.config import config, redis, tokenizer, trigram_repository
from src.utils import strings_has_equal_letters, capitalize


class ReplyGenerator:
    """
    Handles generation of responses for user message
    """
    def __init__(self):
        self.redis = redis
        self.tokenizer = tokenizer
        self.trigram_repository = trigram_repository

        self.max_wrds  = config.getint('grammar', 'max_wrds')
        self.max_msgs  = config.getint('grammar', 'max_msgs')

        self.stop_word = config['grammar']['stop_word']
        self.separator = config['grammar']['separator']
        self.endsen    = config['grammar']['endsen']

    def generate(self, message):
        """
        Generates response based on given message

        :param message: Message
        :return:
                - response (a message) 
                - empty string (if response == message)
        """
        
        words = self.tokenizer.extract_words(message)
        
        # TODO explain this
        pairs = [trigram[:-1] for trigram in self.tokenizer.split_to_trigrams(words)]
        
        # TODO explain why it returns what it returns
        messages = [self.__generate_best_message(chat_id=message.chat_id, pair=pair) for pair in pairs]
        longest_message = max(messages, key=len) if len(messages) else ''
        if longest_message and strings_has_equal_letters(longest_message, ''.join(words)):
            return ''

        return longest_message

    def __generate_best_message(self, chat_id, pair):
        # TODO explain this method
        best_message = ''
        for _ in range(self.max_msgs):
            generated = self.__generate_sentence(chat_id=chat_id, pair=pair)
            if len(generated) > len(best_message):
                best_message = generated
        # TODO explain the concept of the BEST message 
        return best_message

    def __generate_sentence(self, chat_id, pair):
        # TODO explain this method
        gen_words = []
        key = self.separator.join(pair)

        # TODO explain this loop
        for _ in range(self.max_wrds):
            words = key.split(self.separator)

            gen_words.append(words[1] if len(gen_words) == 0 else words[1])

            next_word = self.trigram_repository.get_random_reply(chat_id, key)
            if next_word is None:
                break

            key = self.separator.join(words[1:] + [next_word])

        # TODO explain what's last word
        # Append last word unless it is in the list already
        last_word = key.split(self.separator)[-1]
        if last_word not in gen_words:
            gen_words.append(last_word)

        # If all words are equal (if set(words) == words[0]), leave just 1 word
        if len(set(gen_words)) == 1:
            gen_words = list(set(gen_words))

        gen_words = [w for w in gen_words if w != self.stop_word]
        # TODO maybe move wordlist preparations to some function?

        # TODO maybe move generating the sentence to a function?
        sentence = ' '.join(gen_words).strip()
        if sentence[-1:] not in self.endsen:
            # TODO explain this pls:
            sentence += self.tokenizer.random_end_sentence_token()
        # sentence = capitalize(sentence) 
        # TODO my intuition tells me we shouldn't return fun(obj), but IDK really

        return sentence
