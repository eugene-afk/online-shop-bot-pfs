from aiogram import types

from ..instance import dp, bot
from ..services.orders import OrdersService
from logger import logger
from models.order import OrderStatus

@dp.callback_query_handler(lambda c: c.data and c.data.startswith('sendorder'))
async def notify_user_order_status_sended(callback_query: types.CallbackQuery):
    order_id = callback_query.data.split(";")[1]
    try:
        service = OrdersService()
        service.create_or_set_session()
        order = await service.get_order(order_id)
        if not order:
            return await bot.send_message(callback_query.from_user.id, "Error occured while updating order status. Try again later.")

        await service.update_order_status(OrderStatus.Sended, order_id)
        order_products = [f"- Name: {i.product.name}, Qty: {i.qty}, Total price: {i.total_price} UAH\n" for i in order.products]
        order_products_str = ";".join(order_products)

        #TODO: move message to a separate file for messages
        await bot.send_message(order.user_id, f"""Order #{order.id} was sended. Order Information:
User: {order.user.name}
Shipping address: {order.country_code} {order.state} {order.city} {order.street_line1} {order.street_line2}
{order.post_code}
Shipping method: {order.shipping_option_id}
Shipping cost: {order.shipping_price} UAH
Products:
{order_products_str}
Amount: {order.total_amount} UAH
""")
        
    except Exception as ex:
        logger.exception(ex)
        return await bot.send_message(callback_query.from_user.id, "Error occured while updating order status. Try again later.")
    finally:
        await service.close_session()


