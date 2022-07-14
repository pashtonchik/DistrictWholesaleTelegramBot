from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


is_pay = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Оплатил)', callback_data='is_paid')
        ],
        [
            InlineKeyboardButton(text='Отменить заказ(', callback_data='cancel')
        ],
    ],
    resize_keyboard=True
)
