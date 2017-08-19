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
        self.sep       = config['grammar']['sep']
        self.endsen    = config['grammar']['endsen']

    def generate(self, message):
        """
        Generates response based on given message

        :param message: Message
        :return:
                - response (a message) 
                - None (if response == message or no message chains was generated)
        """
        
        words = self.tokenizer.extract_words(message)
        
        # TODO explain this
        """
        Преобразовываем триграммы в пары слов, чтобы было проще составлять цепочку.
        Например [('hello', 'how', 'do'), ('do', 'you', 'feel'), ('feel', 'today', None)] станет
         вот таким [('hello', 'how'), ('do', 'you'), ('feel', 'today')]
        """
        pairs = [trigram[:-1] for trigram in self.tokenizer.split_to_trigrams(words)]

        # TODO explain why it returns what it returns
        """
        Генерирует цепочку для КАЖДОЙ пары слов.
        Причины для возвращения самого длинного сообщения из всех - нет,
         на тот момент казалось что это наилучший вариант
        """
        messages = [self.__generate_best_message(chat_id=message.chat_id, pair=pair) for pair in pairs]
        longest_message = max(messages, key=len) if len(messages) else None

        if longest_message and strings_has_equal_letters(longest_message, ''.join(words)):
            return None

        return longest_message

    def __generate_best_message(self, chat_id, pair):
        # TODO explain this method
        """
        Метод генерирует несколько (максимум self.max_msgs) различных предложений,
        и оставляет лишь то, которое длиннее всех
        """
        best_message = ''
        for _ in range(self.max_msgs):
            generated = self.__generate_sentence(chat_id=chat_id, pair=pair)
            if len(generated) > len(best_message):
                best_message = generated
        # TODO explain the concept of the BEST message
        """
        У кого длиннее - тот и победил. Самый тупой алгоритм на свете
        """
        return best_message

    def __generate_sentence(self, chat_id, pair):
        # TODO explain this method
        gen_words = []
        key = self.sep.join(pair)

        # TODO explain this loop
        """
        Например приходит пара (привет, бот)
        Мы ее преобразуем в строку 'привет$бот' и пишем в key.
        Затем итерируемся максимум 50 раз. На каждой итерации:
        
        1. Преобразуем ключ обратно в пару, 'привет$бот' станет вновь (привет, бот)
        2. Добавляем в gen_words второе или первое слово из пары, в зависимости от размера gen_words (Вот это как раз и формирует результат)
        3. Получаем случайное слово используя пару привет$бот.
        4.1. Если слово не нашлось, то прерываем цикл, это означает что у этой пары нет соотношений в базе
        4.2. Если слово нашлось, например 'пидор' то формируем новый ключ из пары, например тут станет бот$пидор (key ВСЕГДА будет состоять из 2-х слов) и повторяем
        """
        for _ in range(self.max_wrds):
            words = key.split(self.sep)

            # Исправил ошибку тут !!!!!!
            gen_words.append(words[0] if len(gen_words) == 0 else words[1])

            next_word = self.trigram_repository.get_random_reply(chat_id, key)
            if next_word is None:
                break

            key = self.sep.join(words[1:] + [next_word])

        # TODO explain what's last word
        # Самое последнее слово в сегенирированном ключе
        # Append last word unless it is in the list already
        last_word = key.split(self.sep)[-1]
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
            """
            Если в конце сформированного предложения нету пунктуации (?!.) (мы ведь не вырезаем эти символы),
             то добавляем ему случайную (?!.) из config.grammar.endsen
            """
            sentence += self.tokenizer.random_end_sentence_token()
        # sentence = capitalize(sentence)
        """
        Чем плохо начало предложения с большой буквы?
        """
        # TODO my intuition tells me we shouldn't return fun(obj), but IDK really
        """
        Не знал о таком стандарте в питоне или что это плохо, зачем лишняя переменная?
        """

        return sentence
