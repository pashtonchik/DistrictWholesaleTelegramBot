from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton, ContentType

from bd_custumers import take_customer, edit_customer, input_all
import data
from freekassa import create_link
from keyboards.inline.yesno import yesorno
from keyboards.inline.edit_profile import edit
from keyboards.inline.yesno import yesorno
import json
from loader import dp, bot
from states.state import setting

PAYMENTS_PROVIDER_TOKEN = '381764678:TEST:38824'


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
    print(data_json)
    message = str()
    total = 0
    for i in data_json:
        summ = int(i['price']) * int(i['quantity'])
        total += summ
        message += f"👟{i['title']} x{i['quantity']} — ₽{summ}\n"
    create_link()
    message += f"Итоговая сумма: ₽{total}\n Ссылка на оплату: ggggg"
    await bot.send_message(webAppMes.chat.id, f"Ваш заказ:\n {message}")
    PRICE = types.LabeledPrice(label='Ваш заказ', amount=total * 100)
    await bot.send_invoice(
        webAppMes.chat.id,
        title='бебра',
        description='вкусная',
        provider_token=PAYMENTS_PROVIDER_TOKEN,
        currency='rub',
        is_flexible=False,  # True если конечная цена зависит от способа доставки
        prices=[PRICE],
        start_parameter='time-machine-example',
        payload='some-invoice-payload-for-our-internal-use'
    )


@dp.pre_checkout_query_handler(lambda query: True)
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    print(pre_checkout_query)
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: types.Message):
    print('successful_payment:')
    pmnt = message.successful_payment.to_python()
    for key, val in pmnt.items():
        print(f'{key} = {val}')

    await bot.send_message(
        message.chat.id,
        'все ок'
    )