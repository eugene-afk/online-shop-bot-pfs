from aiogram.types import BotCommandScopeChat, BotCommand

from ..instance import bot
from .default import get_default_commands

def get_admin_commands() -> list[BotCommand]:
    commands = get_default_commands()

    commands.extend([
        BotCommand('/load_data', 'import products from json'),
    ])

    return commands

async def set_admin_commands(user_id: int):
    await bot.set_my_commands(get_admin_commands(), scope=BotCommandScopeChat(user_id))