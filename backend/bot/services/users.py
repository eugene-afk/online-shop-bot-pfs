from models.user import User

from settings import TELEGRAM_ADMINS
from .base import BaseService
from sqlalchemy import select, update
from logger import logger
class UsersService(BaseService):

    async def get_user(self, id: int) -> User:
        try:
            stmt = select(User).filter(User.id == id)
            result = await self.session.execute(stmt)
            user = result.scalar()
            if not user:
                return None
            
            return user
        except Exception as ex:
            logger.exception(ex)
            return None

    async def create_user(self, id: int, name: str, username: str = None) -> User:
        try:
            new_user = User(
                id=id,
                name=name,
                username= username
            )
            self.session.add(new_user)

            admins = [int(i) if i else 0 for i in TELEGRAM_ADMINS.split(",")]
            if id in admins:
                new_user.is_admin = True

            await self.session.commit()
            await self.session.refresh(new_user)
            self.session.expunge(new_user)

            return new_user
        except Exception as ex:
            logger.exception(ex)
            return None


    async def get_or_create_user(self, id: int, name: str, username: str = None) -> User:
        user = await self.get_user(id)
        if user:
            # update user is_admin in db if settings was changed
            admins = [int(i) if i else 0 for i in TELEGRAM_ADMINS.split(",")]
            if id in admins and not user.is_admin:
                stmt = update(User).filter(User.id == id).values(is_admin=True)
                await self.session.execute(stmt)
                await self.session.commit()
            return user

        return await self.create_user(id, name, username)

