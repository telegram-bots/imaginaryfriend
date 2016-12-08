from .base import Base


class Help(Base):
    name = 'help'

    @staticmethod
    def execute(bot, command):
        Help.reply(
            bot,
            command,
            """Add me to your group and let me listen to your chat for a while.
When I learn enough word pairs, I'll start bringing fun and absurdity to your conversations.

Available commands:
• /ping,
• /get_stats: get the number of word pairs I've learned in this chat,
• /set_chance: set the chance that I'll reply to a random message (must be in range 1-50, default: 5),
• /get_chance: get the current chance of my random reply.

If you get tired of me, you can kick me from the group.
In 12 hours, I'll forget everything that have been learned in your chat, so you can add me again and teach me new things!
"""
        )
