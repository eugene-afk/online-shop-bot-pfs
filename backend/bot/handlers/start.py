from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types.web_app_info import WebAppInfo
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from aiogram import types

from settings import TELEGRAM_WEB_APP_URL
from ..instance import dp
from models.user import User
from ..commands.admin import set_admin_commands

@dp.message_handler(CommandStart())
async def start(message: types.Message, user: User):
    if user.is_admin:
        await set_admin_commands(user.id)

    reply_markup = ReplyKeyboardMarkup().add(KeyboardButton(text="Open Web App", 
        web_app=WebAppInfo(url=f"{TELEGRAM_WEB_APP_URL}/tg/{user.id}"))) # passing to web app user_id needs to personalize data like orders list
    reply_markup.resize_keyboard = True

    await message.answer(text=f"Hello, {user.name}!\nI'm online-shop-bot, test task for PayforSay.", reply_markup=reply_markup)