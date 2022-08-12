from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

# this keyboard uses in message for admins when new order was placed 
def new_order(order_id: int):
    markup = InlineKeyboardMarkup()

    markup.add(InlineKeyboardButton('Send to address.', callback_data=f"sendorder;{order_id}"))

    return markup