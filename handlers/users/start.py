import json

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


def message_discount(discount):
    START_MESSAGE_WITH_DISCOUNT = f'''Приветствую!\n<b>Чтобы заказать продукты нажмите на кнопку.</b>
Напоминаем, что у вас есть скидка {discount}% )
<b>Если при покупке возникли вопросы 
или Вы нашли ошибку, пишите нам!</b>
Телеграм <b>тех. поддержки</b>: t.me/a5caff8b53cbd89e51822f1c3e0e66d2
                            '''
    return START_MESSAGE_WITH_DISCOUNT


@dp.message_handler(CommandStart())
async def bot_start(message: types.Message):
    a = requests.get(f'https://onetwosneaker.ru/api2/customers/?tg_id={message.from_user.id}')
    if a.text != '[]':
        client_info = json.loads(a.text)
        if client_info[0]['discount']:
            await message.answer(text=message_discount(client_info[0]['discount']),
                                 reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(
                                     KeyboardButton(text='Заказать продукты', web_app=WebAppInfo(url=config.WEB_APP_URL))
                                     ), parse_mode='HTML', disable_web_page_preview=True)
        else:
            await message.answer(text=START_MESSAGE,
                                 reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(
                                     KeyboardButton(text='Заказать продукты', web_app=WebAppInfo(url=config.WEB_APP_URL))
                                     ), parse_mode='HTML', disable_web_page_preview=True)
    else:
        await message.answer(text='Необходимо пройти регистрацию \n Как к вам обращаться?')
        await Setting.set_fio.set()
