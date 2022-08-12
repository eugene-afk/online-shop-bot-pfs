from aiogram.types import BotCommandScopeDefault, BotCommand

from ..instance import bot

def get_default_commands() -> list[BotCommand]:
    commands = [
        BotCommand('/start', 'start bot'),
    ]

    return commands

async def set_default_commands():
    await bot.set_my_commands(get_default_commands(), scope=BotCommandScopeDefault())
