from aiogram.dispatcher import Dispatcher
from aiogram import Bot
from aiogram.contrib.fsm_storage.memory import MemoryStorage

from settings import TELEGRAM_API_TOKEN

bot = Bot(token=TELEGRAM_API_TOKEN)
dp = Dispatcher(bot, storage=MemoryStorage())



