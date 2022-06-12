import sqlite3

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, ReplyKeyboardMarkup, KeyboardButton

from loader import dp
from states.state import setting


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    conn = sqlite3.connect('customers.db')
    cur = conn.cursor()
    info = cur.execute('SELECT * FROM customers WHERE tgid=?', (message.from_user.id,))
    if info.fetchone() is None:
        await message.answer('Вы новый пользователь, введите данные о себе \n Для начала введите ФИО')
        await setting.set_fio.set()
    else:
        await message.answer('Чтобы заказать кроссовки перейдите по ссылке',
                                reply_markup=ReplyKeyboardMarkup().add(KeyboardButton(text='Заказать кроссовки',
                                web_app=WebAppInfo(url='https://zingy-flan-23354b.netlify.app/'))).add(KeyboardButton(
                                    text='Меню'
                                )))
