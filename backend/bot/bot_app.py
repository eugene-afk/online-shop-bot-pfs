import asyncio
from aiogram.utils import executor
from aiogram.dispatcher import Dispatcher
from .middlewares.users import UsersMiddleware

from database import create_db
from .instance import dp
from .commands.default import set_default_commands

async def on_bot_start_up(dispatcher: Dispatcher) -> None:
    await create_db()
    await set_default_commands()

def start_bot():
    dp.middleware.setup(UsersMiddleware())
    executor.start_polling(dp, skip_updates=True, on_startup=on_bot_start_up)

if __name__ == '__main__':
    pass
    #start_bot()