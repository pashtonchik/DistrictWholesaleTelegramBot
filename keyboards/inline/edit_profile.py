from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


edit = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text='Редактировать ФИО', callback_data='edit_fio')
        ],
        [
            InlineKeyboardButton(text='Редактировать телефон', callback_data='edit_telephone')
        ],
        [
            InlineKeyboardButton(text='Редактировать адрес доставки', callback_data='edit_adress')
        ],
        # [
        #     InlineKeyboardButton(text='Назад', callback_data='back')
        # ],
    ],
    resize_keyboard=True
)