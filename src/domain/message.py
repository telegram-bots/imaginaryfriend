import random
from src.utils import deep_get_attr


class Message:
    def __init__(self, chat, message, config):
        self.chat    = chat
        self.message = message
        self.config  = config

        if self.has_text():
            self.text = message.text
            self.words = self.__get_words()
        else:
            self.text = ''

    def has_text(self):
        """Returns True if the message has text.
        """
        return self.message.text != ''

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

    def has_anchors(self):
        """Returns True if the message contains at least one anchor from anchors config.
        """
        anchors = self.config['bot']['anchors'].split(',')
        return self.has_text() and \
               (any(x in self.message.text.split(' ') for x in anchors))

    def is_private(self):
        """Returns True if the message is private.
        """
        return self.message.chat.type == 'private'

    def is_reply_to_bot(self):
        """Returns True if the message is a reply to bot.
        """
        user_name = deep_get_attr(self.message, 'reply_to_message.from_user.username')

        return user_name == self.config['bot']['name']

    def is_random_answer(self):
        """Returns True if reply chance for this chat is high enough
        """
        return random.randint(0, 100) < getattr(self.chat, 'random_chance', self.config['bot']['default_chance'])

    def __get_words(self):
        text = list(self.text)

        for entity in self.message.entities:
            text[entity.offset:entity.length] = ' ' * entity.length

        return list(filter(None, map(lambda x: x.lower(), ''.join(text).split(' '))))
