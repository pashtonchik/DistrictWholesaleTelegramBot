from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton

from bd_custumers import take_customer, edit_customer, input_all
from keyboards.inline.yesno import yesorno
from keyboards.inline.edit_profile import edit
from keyboards.inline.yesno import yesorno

from loader import dp, bot
from states.state import setting


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

@dp.message_handler(content_types="web_app_data") #получаем отправленные данные
async def answer(webAppMes: types.WebAppData):
   print(webAppMes) #вся информация о сообщении
   print(webAppMes.web_app_data.data) #конкретно то что мы передали в бота
   await bot.send_message(webAppMes.chat.id, f"получили инофрмацию из веб-приложения: {webAppMes.web_app_data.data}")
   #отправляем сообщение в ответ на отправку данных из веб-приложения