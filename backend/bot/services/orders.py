from sqlalchemy import select, update
from sqlalchemy.orm import selectinload
from aiogram.types.shipping_address import ShippingAddress

from .base import BaseService
from models.order import Order, OrderProduct, OrderStatus
from models.product import Product
from logger import logger

class OrdersService(BaseService):

    async def get_order(self, id: int) -> Order:
        try:
            stmt = select(Order).filter(Order.id == id).options(selectinload(Order.products).selectinload(OrderProduct.product), selectinload(Order.user))
            result = await self.session.execute(stmt)
            order = result.scalar()
            if not order:
                return None

            return order
        except Exception as ex:
            logger.exception(ex)
            return None

    # TODO: add validator for order_dict
    async def create_order(self, order_dict) -> Order:
        try:
            new_order = Order(**order_dict)
            self.session.add(new_order)

            await self.session.commit()
            await self.session.refresh(new_order)
            self.session.expunge(new_order)

            return new_order
        except Exception as ex:
            logger.exception(ex)
            return None

    # TODO: add validator for products
    async def add_order_products(self, products, order_id: int) -> Order:
        try:
            for i in products:
                order_product = OrderProduct(
                    qty=i["qty"],
                    product_id=i["id"],
                    total_price=i["total"],
                    order_id=order_id
                )
                self.session.add(order_product)
                await self.session.commit()

            return await self.get_order(order_id)
        except Exception as ex:
            logger.exception(ex)
            return None

    # TODO: add validator for shipping_data
    async def update_order_shipping_data(self, shipping_data: ShippingAddress, order_id: int) -> Order:
        try:
            stmt = update(Order).filter(Order.id == order_id).values(
                country_code=shipping_data.country_code,
                state=shipping_data.state,
                city=shipping_data.city,
                street_line1=shipping_data.street_line1,
                street_line2=shipping_data.street_line2,
                post_code=shipping_data.post_code,
            )

            await self.session.execute(stmt)
            await self.session.commit()

            return await self.get_order(order_id)
        except Exception as ex:
            logger.exception(ex)
            return None

    async def update_order_shipping_option(self, shipping_option, shipping_price, order_id: int) -> Order:
        try:
            stmt = update(Order).filter(Order.id == order_id).values(shipping_option_id=shipping_option, shipping_price=shipping_price)

            await self.session.execute(stmt)
            await self.session.commit()

            return await self.get_order(order_id)
        except Exception as ex:
            logger.exception(ex)
            return None

    async def update_to_payed_order(self, amount, order_id: int) -> Order:
        try:
            stmt = update(Order).filter(Order.id == order_id).values(total_amount=amount, status=OrderStatus.Pending)
            await self.session.execute(stmt)

            order = await self.get_order(order_id)
            '''decreasing products stock availability. 
                In this app is not necessary beacause those data will be anyway rewritten by next /load_data command.
            '''
            for i in order.products:
                new_qty = i.product.stock_qty - i.qty
                if new_qty < 0:
                    new_qty = 0
                stmt = update(Product).filter(Product.id == i.product.id).values(stock_qty=new_qty)
                await self.session.execute(stmt)

            await self.session.commit()
            return await self.get_order(order_id)
        except Exception as ex:
            logger.exception(ex)
            return None

    async def update_order_status(self, status: OrderStatus, id: int) -> Order:
        try:
            stmt = update(Order).filter(Order.id == id).values(status=status)

            await self.session.execute(stmt)
            await self.session.commit()

            return await self.get_order(id)
        except Exception as ex:
            logger.exception(ex)
            return None
