from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


edit_address = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Все верно', callback_data='good_address')
        ],
        [
            InlineKeyboardButton(text='Изменить улицу', callback_data='edit_street')
        ],
        [
            InlineKeyboardButton(text='Изменить дом', callback_data='edit_house')
        ],
        [
            InlineKeyboardButton(text='Изменить квартиру', callback_data='edit_flat')
        ],
    ],
    resize_keyboard=True
)