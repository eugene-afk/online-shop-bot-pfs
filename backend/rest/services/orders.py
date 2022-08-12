from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status as fa_status, Response 
from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from aiogram import Bot
from io import BytesIO
import xlsxwriter, json

from database import get_session
from logger import logger
from models.order import Order, OrderStatus, OrderProduct
from ..schemas.orders import OrderSchemaXls
from models.user import User
from settings import TELEGRAM_API_TOKEN
from ..schemas.orders import UpdateOrderStatusSchema

class OrdersService:
    def __init__(self, session: AsyncSession = Depends(get_session)) -> List[Order]:
        self.session = session

    #TODO: add pagination
    async def get_orders(self, status: str = "", desc: int = 1, search_user_name: str = "", user_id: int = 0) -> List[Order]:
        try:
            is_admin = await self.__is_admin(user_id)
            stmt = select(Order).options(selectinload(Order.products).selectinload(OrderProduct.product), selectinload(Order.user)).filter(Order.status != OrderStatus.Unpaid)
            if not is_admin:
                stmt = stmt.filter(Order.user_id == user_id)
            if status: 
                stmt = stmt.filter(Order.status == OrderStatus[status]) #TODO: check if status str can be converted to enum
            if search_user_name and is_admin:
                stmt = stmt.join(Order.user).filter(User.name.like(f'%{search_user_name}%'))
            if desc:
                stmt = stmt.order_by(Order.created_at.desc())
            else:
                stmt = stmt.order_by(Order.created_at)

            result = await self.session.execute(stmt)
            return {"is_admin": is_admin, "orders": result.scalars().all()}
        except Exception as ex:
            logger.exception(ex)
            raise HTTPException(status_code=fa_status.HTTP_400_BAD_REQUEST)

    async def update_status(self, data: UpdateOrderStatusSchema):
        try:
            is_admin = self.__is_admin(data.from_user_id)
            if not is_admin:
                raise HTTPException(status_code=fa_status.HTTP_400_BAD_REQUEST)            
            new_status = OrderStatus[data.status] #TODO: check if status str can be converted to enum
            stmt = update(Order).filter(Order.id == data.order_id).values(status=new_status)
            await self.session.execute(stmt)
            await self.session.commit()

            bot = Bot(token=TELEGRAM_API_TOKEN)
            await bot.send_message(data.user_id, f"Status of Order #{data.order_id} was changed to {new_status.name}.")
            await bot.close()
            
            return Response(status_code=200)
        except Exception as ex:
            logger.exception(ex)
            raise HTTPException(status_code=fa_status.HTTP_400_BAD_REQUEST)

    async def make_excel_file(self, filename: str, user_id: int = 0, status: str = "", desc: int = 1, search: str = ""):
        try:
            is_admin = await self.__is_admin(user_id)
            if not is_admin:
                raise HTTPException(status_code=fa_status.HTTP_400_BAD_REQUEST)

            # creating file like object with xlsx file, gettings filtered orders
            output = BytesIO()
            workbook = xlsxwriter.Workbook(output)
            worksheet = workbook.add_worksheet()
            orders_data = await self.get_orders(user_id=327721042, status=status, desc=desc, search_user_name=search)

            # converting orders dict to xlsx
            data = []
            for i in orders_data["orders"]:
                d = i.__dict__
                d["address"] = f"{d['country_code']} {d['state']} {d['city']} {d['street_line1']} {d['street_line2']} {d['post_code']}"
                d["order_status"] = OrderStatus(d["status"]).name
                d["user_id"] = i.user_id
                d["username"] = i.user.name
                data.append(json.loads(OrderSchemaXls(**d).json())) 
                
            await self.__json_to_excel(worksheet, data)
            workbook.close()

            return Response(content=output.getvalue(), 
                media_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet", 
                headers={
                'Content-Disposition': f'attachment; filename={filename}.xlsx'
            })
        except Exception as ex:
            logger.exception(ex)
            raise HTTPException(status_code=fa_status.HTTP_400_BAD_REQUEST)


    async def __json_to_excel(self, ws, data, row=0, col=0):
        if isinstance(data, list):
            row -= 1
            for value in data:
                row = await self.__json_to_excel(ws, value, row+1, col)
        elif isinstance(data, dict):
            max_row = row
            start_row = row
            for key, value in data.items():
                row = start_row
                ws.write(row, col, key)
                row = await self.__json_to_excel(ws, value, row+1, col)
                max_row = max(max_row, row)
                col += 1
            row = max_row
        else:
            ws.write(row, col, data)

        return row

    # I placed this method here because it needs only here, in a real app it should be user, auth modules, decorators for endpoints
    async def __is_admin(self, id: int):
        stmt = select(User).filter(User.id == id)
        result = await self.session.execute(stmt)
        user = result.scalar()
        if user:
            if user.is_admin:
                return True
        return False