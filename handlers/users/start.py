import sqlite3

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, WebAppInfo, ReplyKeyboardMarkup, KeyboardButton

from loader import dp
from states.state import setting

START_MESSAGE = '''Приветствую!\n<b>Чтобы заказать кроссовки нажмите на кнопку.</b>

<b>Если при покупке возникли вопросы 
или Вы нашли ошибку, пишите нам!</b>
Телеграм <b>тех. поддержки</b>: t.me/a5caff8b53cbd89e51822f1c3e0e66d2
                            '''

@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    await message.answer(text=START_MESSAGE, 
    reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(KeyboardButton(text='Заказать кроссовки', web_app=WebAppInfo(url='https://zingy-flan-23354b.netlify.app/'))
                        ),parse_mode='HTML', disable_web_page_preview=True)
