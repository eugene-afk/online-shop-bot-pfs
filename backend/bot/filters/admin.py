from aiogram.dispatcher.filters import BoundFilter
from aiogram.types import Message

from ..services.users import UsersService

class Admin(BoundFilter):
    key = 'is_admin'

    def __init__(self, is_admin: bool):
        self.is_admin = is_admin

    async def check(self, message: Message):
        if 'db_user' not in message:
            service = UsersService()
            service.create_or_set_session()
            message['db_user'] = await service.get_user(message.from_user.id)
            await service.close_session()
        user = message['db_user']

        if not user:
            return False

        return user.is_admin == self.is_admin