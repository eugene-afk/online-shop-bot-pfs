from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import Depends, HTTPException, status
from sqlalchemy import select

from database import get_session
from logger import logger
from models.product import Product
from models.category import Category

class ProductsService:
    def __init__(self, session: AsyncSession = Depends(get_session)) -> List[Product]:
        self.session = session

    #TODO: add pagination
    async def get_products(self, category_id: int = 0, srch_name: str = ""):
        try:
            stmt = select(Product)
            if category_id > 0:
                stmt = stmt.filter(Product.category_id == category_id)
            if srch_name:
                stmt = stmt.filter(Product.name.like(f'%{srch_name}%'))
            stmt = stmt.order_by(Product.stock_qty.desc())
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except Exception as ex:
            logger.exception(ex)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)

    async def get_categories(self) -> List[Category]:
        try:
            stmt = select(Category)
            result = await self.session.execute(stmt)
            return result.scalars().all()
        except Exception as ex:
            logger.exception(ex)
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST)