from src.handler.commands.base import Base
from src.handler.commands.start import Start
from src.handler.commands.help import Help
from src.handler.commands.ping import Ping
from src.handler.commands.get_stats import GetStats
from src.handler.commands.moderate import Moderate
from src.handler.commands.chance import Chance

commands = {}
for clazz in Base.__subclasses__():
    command_name = getattr(clazz, 'name')
    command_aliases = getattr(clazz, 'aliases')
    execute_method = getattr(clazz, 'execute')

    commands[command_name] = execute_method
    for command_alias in command_aliases:
        commands[command_alias] = execute_method
