from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton

from bd_custumers import take_customer, edit_customer, input_all
import data
from keyboards.inline.yesno import yesorno
from keyboards.inline.edit_profile import edit
from keyboards.inline.yesno import yesorno
import json
from loader import dp, bot
from states.state import setting

from freekassa import FreeKassaApi
import requests

client = FreeKassaApi(
    first_secret='z$LLtY$7C<oiOpF',
    second_secret='!UZi(zYI3E63/&[',
    merchant_id='13d0bfab8dd487182cf417977fe8470c',
    wallet_id='18316')


@dp.message_handler(text='Меню')
async def check_fio(message: types.Message, state=FSMContext):
    data = take_customer(message.from_user.id)
    msg = f'''
ФИО: {data[0][1]}
Телефон: {data[0][2]}
Адрес доставки: {data[0][4]} 
'''
    await message.answer(text=msg, reply_markup=edit)
    await setting.check_profile.set()


@dp.callback_query_handler(state=setting.check_profile)
async def edit_profile(call: types.CallbackQuery, state=FSMContext):
    if call.data == 'edit_fio':
        await call.message.edit_text(text='Введите новое ФИО:', reply_markup='')
        await setting.edit_fio.set()
    elif call.data == 'edit_telephone':
        await call.message.edit_text(text='Введите новый номер телефона:', reply_markup='')
        await setting.edit_telephone.set()
    elif call.data == 'edit_adress':
        await call.message.edit_text(text='Введите новый адрес доставки:', reply_markup='')
        await setting.edit_adress.set()
    elif call.data == 'back':
        await call.message.edit_text('Чтобы заказать кроссовки перейдите по ссылке',
                                reply_markup=InlineKeyboardMarkup().add(InlineKeyboardButton(text='Заказать кроссовки',
                                web_app=WebAppInfo(url='https://zingy-flan-23354b.netlify.app/'))).add(InlineKeyboardButton(
                                    text='Посмотреть свой профиль', callback_data='check_profile'
                                )))
        await state.finish()


@dp.message_handler(state=setting.edit_fio)
async def check_fio(message: types.Message):
    edit_customer('fio', message.from_user.id, message.text)
    data = take_customer(message.from_user.id)
    msg = f'''
ФИО: {data[0][1]}
Телефон: {data[0][2]}
Адрес доставки: {data[0][4]} 
    '''
    await message.answer(text=msg, reply_markup=edit)
    await setting.check_profile.set()


@dp.message_handler(state=setting.edit_telephone)
async def check_fio(message: types.Message):
    edit_customer('tel', message.from_user.id, message.text)
    data = take_customer(message.from_user.id)
    msg = f'''
ФИО: {data[0][1]}
Телефон: {data[0][2]}
Адрес доставки: {data[0][4]} 
    '''
    await message.answer(text=msg, reply_markup=edit)
    await setting.check_profile.set()


@dp.message_handler(state=setting.edit_adress)
async def check_fio(message: types.Message):
    edit_customer('adress', message.from_user.id, message.text)
    data = take_customer(message.from_user.id)
    msg = f'''
ФИО: {data[0][1]}
Телефон: {data[0][2]}
Адрес доставки: {data[0][4]} 
    '''
    await message.answer(text=msg, reply_markup=edit)
    await setting.check_profile.set()


@dp.message_handler(content_types="web_app_data")
async def answer(webAppMes: types.WebAppData):
    data_json = json.loads(webAppMes.web_app_data.data)
    balance = client.get_balance()
    print(balance.text)
    print(data_json)
    message = str()
    total = 0
    for i in data_json:
        total += int(i['price'])
        message += f"👟{i['title']} x{i['quantity']} — ₽{i['price']}\n"
    data = requests.get('https://pay.freekassa.ru/')
    summ = '100'
    order_id = '1111'
    email = 'pashka191@yandex.ru'
    description = ''
    payment_link = client.generate_payment_link(order_id, summ, email, description)
    message += f"Итоговая сумма: ₽{total}\n Ссылка на оплату: {payment_link}"
    await bot.send_message(webAppMes.chat.id, f"Ваш заказ:\n {message}")
    print(payment_link)
    