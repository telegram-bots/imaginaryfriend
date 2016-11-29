import random
import re
from urllib.parse import urlparse
from .abstract_entity import AbstractEntity
from src.utils import deep_get_attr
from src.config import config


class Message(AbstractEntity):
    def __init__(self, chat, message):
        super(Message, self).__init__(chat=chat, message=message)

        if self.has_text():
            self.text = message.text
            self.links = self.__get_links()
            self.words = self.__get_words()
        else:
            self.text = ''
            self.links = []
            self.words = []

    def has_text(self):
        """Returns True if the message has text.
        """
        return self.message.text.strip() != ''

    def is_sticker(self):
        """Returns True if the message is a sticker.
        """
        return self.message.sticker is not None

    def is_editing(self):
        """Returns True if the message was edited.
        """
        return self.message.edit_date is not None

    def has_entities(self):
        """Returns True if the message has entities (attachments).
        """
        return self.message.entities is not None

    def has_links(self):
        return len(self.links) != 0

    def has_anchors(self):
        """Returns True if the message contains at least one anchor from anchors config.
        """
        anchors = config.getlist('bot', 'anchors')
        return self.has_text() and any(a in self.message.text.split(' ') for a in anchors)

    def is_private(self):
        """Returns True if the message is private.
        """
        return self.message.chat.type == 'private'

    def is_reply_to_bot(self):
        """Returns True if the message is a reply to bot.
        """
        user_name = deep_get_attr(self.message, 'reply_to_message.from_user.username')

        return user_name == config['bot']['name']

    def is_random_answer(self):
        """Returns True if reply chance for this chat is high enough
        """
        return random.randint(0, 100) < getattr(self.chat, 'random_chance', config['bot']['default_chance'])

    def should_answer(self):
        return self.has_anchors() \
            or self.is_private() \
            or self.is_reply_to_bot() \
            or self.is_random_answer()

    def __get_links(self):
        links = []

        def prettify(url):
            if not url.startswith('http://') and not url.startswith('https://'):
                url = 'http://' + url

            link = urlparse(url)
            host = '.'.join(link.hostname.split('.')[-2:])
            return '{}{}#{}'.format(host, link.path, link.fragment)

        for entity in filter(lambda e: e.type == 'url', self.message.entities):
            link = prettify(self.text[entity.offset:entity.length + entity.offset])
            links.append(link)

        return links

    def __get_words(self):
        symbols = list(re.sub('\s', ' ', self.text))

        def prettify(word):
            lowercase_word = word.lower().strip()
            last_symbol = lowercase_word[-1:]
            if last_symbol not in config['grammar']['end_sentence']:
                last_symbol = ''
            pretty_word = lowercase_word.strip(config['grammar']['all'])

            if pretty_word != '' and len(pretty_word) > 2:
                return pretty_word + last_symbol
            elif lowercase_word in config['grammar']['all']:
                return None

            return lowercase_word

        for entity in self.message.entities:
            symbols[entity.offset:entity.length + entity.offset] = ' ' * entity.length

        return list(filter(None, map(prettify, ''.join(symbols).split(' '))))
