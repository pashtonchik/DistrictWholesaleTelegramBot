from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart
from aiogram.types import WebAppInfo, ReplyKeyboardMarkup, KeyboardButton
import requests

from data import config
from loader import dp
from states.state import Setting


START_MESSAGE = '''Приветствую!\n<b>Чтобы заказать продукты нажмите на кнопку.</b>

<b>Если при покупке возникли вопросы 
или Вы нашли ошибку, пишите нам!</b>
Телеграм <b>тех. поддержки</b>: t.me/a5caff8b53cbd89e51822f1c3e0e66d2
                            '''


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    a = requests.get(f'https://onetwosneaker.ru/api2/customers/?tg_id={message.from_user.id}')
    if a.text != '[]':
        await message.answer(text=START_MESSAGE,
                             reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(
                                 KeyboardButton(text='Заказать продукты', web_app=WebAppInfo(url=config.WEB_APP_URL))
                                 ), parse_mode='HTML', disable_web_page_preview=True)
    else:
        await message.answer(text='Необходимо пройти регистрацию \n Как к вам обращаться?')
        await Setting.set_fio.set()
