from telegram.ext import Handler
from telegram import Update
from src.domain.chat import Chat


class CommandHandler(Handler):
    def __init__(self, allow_edited = False, pass_update_queue = False, pass_job_queue=False, 
                       pass_user_data = False, pass_chat_data = False):      
        super(CommandHandler, self).__init__(self.handle, 
                                             pass_update_queue = pass_update_queue,
                                             pass_job_queue    = pass_job_queue, 
                                             pass_user_data    = pass_user_data,
                                             pass_chat_data    = pass_chat_data)
        
        self.allow_edited = allow_edited
        self.commands = {
            'start':      self.__start_command,
            'help':       self.__help_command,
            'ping':       self.__ping_command,
            'set_chance': self.__set_chance_command,
            'get_chance': self.__get_chance_command,
            'get_stats':  self.__get_stats_command
        }

    
    def check_update(self, update):
        if isinstance(update, Update) and (update.message or update.edited_message and self.allow_edited):
            message = update.message or update.edited_message

            return (message.text and message.text.startswith('/') and self.__parse_command_name(update) in self.commands)
        else:
            return False

        
    def handle_update(self, update, dispatcher):
        optional_args = self.collect_optional_args(dispatcher, update)
        message = update.message or update.edited_message
        optional_args['args'] = message.text.split()[1:]

        return self.callback(dispatcher.bot, update, **optional_args)


    def handle(self, bot, update, args):
        try:
            command = self.__parse_command_name(update)
            method = self.commands[command]
            method(update, args)
        except (IndexError, ValueError):
            update.message.reply_text('Invalid command!')

            
    def __parse_command_name(self, update):
        message = update.message or update.edited_message

        return message.text[1:].split(' ')[0].split('@')[0]

    
    def __start_command(self, update, args):
        update.message.reply_text('Hi! :3')

        
    def __help_command(self, update, args):
        update.message.reply_text(
            """Available commands:
            • /ping,
            • /get_stats: get information on how many pairs are known by ImaginaryFriend,
            • /set_chance: set the probability that ImaginaryFriend would reply to a random message (must be in range 1-50, default: 5),
            • /get_chance: get current probability that ImaginaryFriend would reply to a message.')"""
        )


    def __ping_command(self, update, args):
        update.message.reply_text('pong')


    def __set_chance_command(self, update, args):
        try:
            random_chance = int(args[0])

            if random_chance < 1 or random_chance > 50:
                raise ValueError

            chat = Chat.get_chat(update.message)
            chat.random_chance = random_chance
            chat.save()

            update.message.reply_text('Set chance to: {}'.format(random_chance))
        except (IndexError, ValueError):
            update.message.reply_text('Usage: /set_chance 1-50')

                                  
    def __get_chance_command(self, update, args):
        update.message.reply_text('Current chance: {}'.format(Chat.get_chat(update.message).random_chance))

                                  
    def __get_stats_command(self, update, args):
        update.message.reply_text('Pairs: {}'.format(Chat.get_chat(update.message).pairs().count()))
