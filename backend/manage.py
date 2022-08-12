from manager import Manager
import asyncio

from asgi import start_rest
from bot.bot_app import start_bot
from database import create_db

manager = Manager()

@manager.command
def run_rest():
    #asyncio.get_event_loop().run_until_complete(create_db())
    start_rest()

@manager.command
def run_bot():
    from bot import filters, handlers 
    start_bot()

if __name__ == '__main__':
    manager.main()