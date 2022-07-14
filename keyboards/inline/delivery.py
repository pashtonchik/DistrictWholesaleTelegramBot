from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


delivery = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Доставка', callback_data='del')
        ],
        [
            InlineKeyboardButton(text='Самовывоз', callback_data='yourself')
        ],
    ],
    resize_keyboard=True
)
