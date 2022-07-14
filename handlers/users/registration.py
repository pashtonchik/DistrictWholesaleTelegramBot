import json

import requests
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton, ReplyKeyboardMarkup, KeyboardButton
from keyboards.inline.yesno import yesorno
from loader import dp
from states.state import Setting

WEB_APP_URL = 'https://dreamy-crisp-137a51.netlify.app/'


@dp.message_handler(state=Setting.set_fio)
async def set_fio(message: types.Message, state=FSMContext):
    fio = message.text
    await message.answer(text=fio + '\n Верно?', reply_markup=yesorno)
    await Setting.check_fio.set()
    await state.update_data(fio=fio)


@dp.callback_query_handler(state=Setting.check_fio)
async def check_fio(call: types.CallbackQuery, state=FSMContext):
    if call.data == 'yes':
        data = await state.get_data()
        print(data)
        await call.message.edit_text(text='Отправьте ваш номер телефона', reply_markup='')
        await Setting.set_telephone.set()
        await state.update_data(fio=data['fio'])
    else:
        await call.message.edit_text(text='Тогда введите имя повторно:', reply_markup='')
        await Setting.set_fio.set()


@dp.message_handler(state=Setting.set_telephone)
async def set_telephone(message: types.Message, state=FSMContext):
    telephone = message.text
    data = await state.get_data()
    print(data)
    await message.answer(text=telephone + '\n Верно?', reply_markup=yesorno)
    await Setting.check_telephone.set()
    await state.update_data(fio=data['fio'], phone_number=telephone)


@dp.callback_query_handler(state=Setting.check_telephone)
async def check_address(call: types.CallbackQuery, state=FSMContext):
    data = await state.get_data()
    print(data)
    print(data['fio'], data['phone_number'])
    if call.data == 'yes':
        print(call.from_user.id)
        body_add_customer = {
            "tg_id": call.from_user.id,
            "name": data['fio'],
            "phone_number": data['phone_number'],
        }
        add_customer = json.dumps(body_add_customer)
        print(add_customer)
        r = requests.post('https://onetwosneaker.ru/api2/addcustomer', data=add_customer)
        await call.message.answer(text='Теперь можете покупать продукты',
                                  reply_markup=ReplyKeyboardMarkup(resize_keyboard=True).add(
                                      KeyboardButton(text='Заказать продукты', web_app=WebAppInfo(url=WEB_APP_URL))
                                  ), parse_mode='HTML', disable_web_page_preview=True)
        await Setting.go_site.set()
    else:
        await call.message.edit_text(text='Тогда отправьте ваш номер телефона ещё раз', reply_markup='')
        await Setting.set_adress.set()
        await state.update_data(fio=data['fio'], phone_number=data['phone_number'])
