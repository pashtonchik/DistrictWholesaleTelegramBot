from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


yesorno = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Да', callback_data='yes')
        ],
        [
            InlineKeyboardButton(text='Нет', callback_data='no')
        ],
    ],
    resize_keyboard=True
)

