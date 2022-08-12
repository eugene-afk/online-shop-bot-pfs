from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from datetime import datetime

from models.category import Category
from .base import BaseService
from models.product import Product
from logger import logger

class ProductsService(BaseService):

    # TODO: add validator product_dict
    async def create_product(self, product_dict) -> Product:
        try:
            new_product = Product(**product_dict)
            self.session.add(new_product)

            await self.session.commit()
            await self.session.refresh(new_product)
            self.session.expunge(new_product)

            return new_product
        except Exception as ex:
            logger.exception(ex)
            return None

    async def get_product_by_name(self, name: str) -> Product:
        try:
            stmt = select(Product).filter(Product.name == name).options(selectinload(Product.category))
            result = await self.session.execute(stmt)
            product = result.scalar()
            if not product:
                return None

            return product
        except Exception as ex:
            logger.exception(ex)
            return None

    async def get_product(self, id: int) -> Product:
        try:
            stmt = select(Product).filter(Product.id == id).options(selectinload(Product.category))
            result = await self.session.execute(stmt)
            product = result.scalar()
            if not product:
                return None

            return product
        except Exception as ex:
            logger.exception(ex)
            return None

    # TODO: add validator for product_dict
    async def update_product(self, product_dict) -> Product:
        try:
            id = product_dict["id"]
            del product_dict["id"]
            stmt = update(Product).filter(Product.id == id).values(**product_dict)

            await self.session.execute(stmt)
            await self.session.commit()

            return await self.get_product(id)
        except Exception as ex:
            logger.exception(ex)
            return None

    # TODO: add validator for data
    async def update_products_by_json(self, data) -> bool:
        try:
            self.create_or_set_session()
            updated_date = datetime.utcnow().replace(microsecond=0)
            
            for i in data:
                cat = await self.get_category_by_id(i["category_id"])
                if not cat:
                    i["category_id"] = 1 # if unknown category - adding to Uncategorized

                i["updated_at"] = updated_date
                prod = await self.get_product_by_name(i["name"])
                if not prod: # creating a new product if it doesn't exists
                    await self.create_product(i) 
                    continue
                i["id"] = prod.id
                await self.update_product(i) # updating product if it exists

            # getting products that were not updated, so it means there not exist in the current json file
            stmt = select(Product).filter(Product.updated_at < updated_date) 
            prods_for_del_res = await self.session.execute(stmt)
            prods_for_del = prods_for_del_res.scalars().all()

            # deleting product that didn't exist in json file
            for i in prods_for_del:
                await self.session.delete(i) 
            await self.session.commit()

            return True
        except Exception as ex:
            logger.exception(ex)
            return False
        finally:
            await self.close_session()

    async def get_category_by_id(self, id) -> Category:
        try:
            stmt = select(Category).filter(Category.id == id)
            result = await self.session.execute(stmt)
            category = result.scalar()
            return category
        except Exception as ex:
            logger.exception(ex)
            return None
