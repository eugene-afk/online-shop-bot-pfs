from aiogram import types
from aiogram.types.message import ContentTypes
import json

from settings import TELEGRAM_PAYMENTS_PROVIDER_TOKEN, TELEGRAM_ADMINS
from ..instance import dp, bot
from logger import logger
from ..services.orders import OrdersService
from ..keyboards.inline import new_order

# Hardcoded shipping options, in real app it should be in database
shipping_options_list = [
    {
        "id": "dhl",
        "title": "DHL",
        "label": "DHL",
        "price": 10000,
    },
    {
        "id": "pickup",
        "title": "Local pickup",
        "label": "Pickup",
        "price": 1000,
    },
]
shipping_options = []
for i in shipping_options_list:
    shipping_options.append(
        types.ShippingOption(id=i["id"], title=i["title"]).add(types.LabeledPrice(i["label"], i["price"]))
    )

@dp.shipping_query_handler(lambda query: True)
async def shipping(shipping_query: types.ShippingQuery):
    try:
        service = OrdersService()
        service.create_or_set_session()
        invoice_payload = json.loads(shipping_query.invoice_payload)
        await service.update_order_shipping_data(shipping_query.shipping_address, invoice_payload["order_id"])
    except Exception as ex:
        logger.exception(ex)
        return await bot.answer_shipping_query(
            shipping_query.id,
            ok=False,
            error_message="Error was occured while updating the order with shipping info. Try again later."
        )
    finally:
        await service.close_session()
    await bot.answer_shipping_query(shipping_query.id, ok=True, shipping_options=shipping_options,
                                    error_message='Oh, seems like our Dog couriers are having a lunch right now.'
                                                  ' Try again later!')


@dp.pre_checkout_query_handler(lambda query: True)
async def checkout(pre_checkout_query: types.PreCheckoutQuery):
    try:
        service = OrdersService()
        service.create_or_set_session()
        invoice_payload = json.loads(pre_checkout_query.invoice_payload)
        shipping_option = next((i for i in shipping_options_list if i["id"] == pre_checkout_query.shipping_option_id), None)

        await service.update_order_shipping_option(pre_checkout_query.shipping_option_id, 
            shipping_option["price"] / 100, 
            invoice_payload["order_id"])
    except Exception as ex:
        logger.exception(ex)
        return await bot.answer_pre_checkout_query(
            pre_checkout_query.id,
            ok=False,
            error_message="Error was occured while updating the order with shipping option. Try again later."
        )
    finally:
        await service.close_session()
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True,
                                        error_message="Aliens tried to steal your card's CVV,"
                                                      " but we successfully protected your credentials,"
                                                      " try to pay again in a few minutes, we need a small rest.")


@dp.message_handler(content_types=ContentTypes.SUCCESSFUL_PAYMENT)
async def got_payment(message: types.Message):
    try:
        service = OrdersService()
        service.create_or_set_session()
        invoice_payload = json.loads(message.successful_payment.invoice_payload)
        order = await service.update_to_payed_order(message.successful_payment.total_amount / 100, invoice_payload["order_id"])

        # sending messages about order to admins
        try:
            order_products = [f"- Name: {i.product.name}, Qty: {i.qty}, Total price: {i.total_price} UAH\n" for i in order.products]
            order_products_str = ";".join(order_products)
            markup = new_order(order.id)

            admins = [int(i) if i else 0 for i in TELEGRAM_ADMINS.split(",")]
            for i in admins:
                if i != 0:
                    await bot.send_message(i, f"""Order #{order.id}. Order Information:
User: {order.user.name}
Shipping address: {order.country_code} {order.state} {order.city} {order.street_line1} {order.street_line2} {order.post_code}
Shipping method: {order.shipping_option_id}
Shipping cost: {order.shipping_price} UAH
Products:
{order_products_str}
Amount: {order.total_amount} UAH
""", reply_markup=markup)
        except Exception as ex:
            logger.exception(ex)
        finally:
            await service.close_session()

        '''
        bad situation when payment was successful, but db query had errors. 
        In a real app here should be some background service call, that will deal with errors and trying to store data. 
        '''
    except Exception as ex:  
        logger.exception(ex)
        return await bot.send_message(message.chat.id, "Your order was successfully payed, but it didn't saved to the database.")
    finally:
        await service.close_session()

    await bot.send_message(message.chat.id, f"Order #{order.id} pending. Soon it will be sended by your address.")

#TODO: add validator for web_app_data
@dp.message_handler(content_types="web_app_data")
async def got_data_from_web_app(message: types.Message):
    '''web_app_data size can be optimized, for example passing only products id without names.
     For Now I'm passing almost all product info to prevent additional db queries'''
    data = json.loads(message.web_app_data.data)
    try:
        service = OrdersService()
        service.create_or_set_session()
        order = await service.create_order({"user_id": message.chat.id}) # creating unpaid order
        
        await service.add_order_products(data, order.id) # adding products to order

        invoice_payload = {"order_id": order.id} # payload for next handlers to update order with new data in db
        prices = []

        for i in data:
            total = i["total"]
            amount = int(float(total) * 100) #TODO: check min and max amount
            prices.append(
                types.LabeledPrice(label=i["name"], amount=amount)
            )
    except Exception as ex:
        logger.exception(ex)
        return await message.answer(text="Error was occured while creating your order. Try again later.")
    finally:
        await service.close_session()

    await bot.send_invoice(message.chat.id,
                    title=f"Order #{order.id}",
                    description="Thanks for choosing our shop!",
                    provider_token=TELEGRAM_PAYMENTS_PROVIDER_TOKEN,
                    currency='uah',
                    photo_url="https://img.freepik.com/premium-vector/happy-shop-logo-template_57516-57.jpg",
                    photo_height=512,
                    photo_width=512,
                    photo_size=512,
                    need_email=True,
                    need_phone_number=True,
                    is_flexible=True,
                    prices=prices,
                    start_parameter='example',
                    payload=json.dumps(invoice_payload))