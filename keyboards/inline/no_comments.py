from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


no_comments = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Без комментария', callback_data='no_comments')
        ],
    ],
    resize_keyboard=True
)