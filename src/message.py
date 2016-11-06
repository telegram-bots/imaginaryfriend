import logging
import random

import src.domain.chat as chat
import src.domain.pair as pair


class Message:
    def __init__(self, bot, message, config):
        self.bot                     = bot
        self.message                 = message
        self.config                  = config
        self.chat                    = chat.Chat.get_chat(message)
        self.chat.migrate_to_chat_id = message.migrate_to_chat_id

        if self.has_text():
            logging.debug("[chat %s %s bare_text] %s" %
                          (self.chat.chat_type, 
                           self.chat.telegram_id, 
                           self.message.text))
            self.text    = message.text
            self.words   = self.__get_words()
            self.command = self.__get_command() if self.text[0] == '/' else None

    def process(self):
        if self.has_text() and not self.is_editing():
            # TODO Implement
            if self.is_command():
                pass
            else:
                return self.__process_message()

    def has_text(self):
        """Returns True if the message has text.
        """
        return self.message.text != ''

    def is_editing(self):
        """Returns True if the message was edited.
        """
        return self.message.edit_date is not None

    def has_entities(self):
        """Returns True if the message has entities (attachments).
        """
        return self.message.entities is not None

    def has_anchors(self):
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
        reply_to_message = getattr(self.message, 'reply_to_message', None)
        from_user        = getattr(reply_to_message, 'from_user', None)
        user_name        = getattr(from_user, 'username', None)

        return user_name == self.config['bot']['name']

    def is_random_answer(self):
        return random.randint(0, 100) < getattr(self.chat, 'random_chance', 5)

    def is_command(self):
        """Returns True if the message is a command (`/start`, `/do_stuff`).
        """
        return self.command is not None

    def __answer(self, message):
        logging.debug("[Chat %s %s answer] %s" %
                      (self.chat.chat_type, 
                       self.chat.telegram_id, 
                       message))
        
        self.bot.sendMessage(chat_id=self.chat.telegram_id, text=message)

    def __reply(self, message):
        logging.debug("[Chat %s %s reply] %s" %
                      (self.chat.chat_type, 
                       self.chat.telegram_id, 
                       message))
        
        self.bot.sendMessage(chat_id=self.chat.telegram_id,
                             reply_to_message_id=self.message.message_id,
                             text=message)

    def __process_message(self):
        pair.Pair.learn(self)

        if self.has_anchors() \
                or self.is_private() \
                or self.is_reply_to_bot() \
                or self.is_random_answer():
            reply = pair.Pair.generate(self)
            if reply != '':
                self.__answer(reply)

    def __get_words(self):
        text = list(self.text)
        
        for entity in self.message.entities:
            text[entity.offset:entity.length] = ' ' * entity.length
        
        result = list(filter(None, map(lambda x: x.lower(), ''.join(text).split(' '))))
        
        logging.debug("[chat %s %s get_words] %s" %
                      (self.chat.chat_type,
                       self.chat.telegram_id, 
                       result))

        return result

    # TODO Implement
    def __get_command(self):
        return None
