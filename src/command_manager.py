from src.domain.chat import Chat


class CommandManager:
    def __init__(self):
        self.commands = {
            'set_chance': self.__set_chance_command
        }

    def handle(self, bot, update, command, args):
        if command in self.commands:
            method = self.commands[command]
            method(update, args)
        else:
            update.message.reply_text('Invalid command!')

    def __set_chance_command(self, update, args):
        try:
            random_chance = int(args[0])

            if random_chance < 1 or random_chance > 50:
                raise ValueError

            chat = Chat.get_chat(update.message)
            chat.random_chance = random_chance
            chat.save()

            update.message.reply_text('Set chance to %d' % random_chance)
        except (IndexError, ValueError):
            update.message.reply_text('Usage: /set_chance 1-50')
