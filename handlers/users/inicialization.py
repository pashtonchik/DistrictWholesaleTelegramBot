from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton

from bd_custumers import insert_customer, input_all
from keyboards.inline.yesno import yesorno

from loader import dp
from states.state import setting

fio = ''
telephone = ''
tgid = ''
adress = ''


@dp.message_handler(state=setting.set_fio)
async def set_fio(message: types.Message, state=FSMContext):
    global fio
    fio = message.text
    await message.answer(text=fio + '\n Верно?', reply_markup=yesorno)
    await setting.check_fio.set()


@dp.callback_query_handler(state=setting.check_fio)
async def check_fio(call: types.CallbackQuery, state=FSMContext):
    if call.data == 'yes':
        await call.message.edit_text(text='Далее введите номер телефона:', reply_markup='')
        await setting.set_telephone.set()
    else:
        await call.message.edit_text(text='Тогда введите ФИО повторно:', reply_markup='')
        await setting.set_fio.set()


@dp.message_handler(state=setting.set_telephone)
async def set_telephone(message: types.Message, state=FSMContext):
    global telephone, tgid
    telephone = message.text
    tgid = message.from_user.id
    await message.answer(text=telephone + '\n Верно?', reply_markup=yesorno)
    await setting.check_telephone.set()


@dp.callback_query_handler(state=setting.check_telephone)
async def check_telephone(call: types.CallbackQuery, state=FSMContext):
    if call.data == 'yes':
        await call.message.edit_text(text='Далее введите адрес доставки:', reply_markup='')
        await setting.set_adress.set()
    else:
        await call.message.edit_text(text='Тогда введите телефон повторно:', reply_markup='')
        await setting.set_telephone.set()


@dp.message_handler(state=setting.set_adress)
async def set_adress(message: types.Message, state=FSMContext):
    global adress
    adress = message.text
    await message.answer(text=adress + '\n Верно?', reply_markup=yesorno)
    await setting.check_adress.set()


@dp.callback_query_handler(state=setting.check_adress)
async def check_adress(call: types.CallbackQuery, state=FSMContext):
    if call.data == 'yes':
        insert_customer((fio, telephone, tgid, adress))
        input_all()
        await call.message.edit_text(text='Теперь осталось только выбрать кроссовки и оформить заказ',
                                  reply_markup=InlineKeyboardMarkup().add(
                                      InlineKeyboardButton(text='Заказать кроссовки',
                                                           web_app=WebAppInfo(
                                                               url='https://zingy-flan-23354b.netlify.app/'))).add(
                                      InlineKeyboardButton(
                                          text='Посмотреть свой профиль', callback_data='check_profile'
                                      )))
        await state.finish()
    else:
        await call.message.edit_text(text='Тогда введите телефон повторно:', reply_markup='')
        await setting.set_adress.set()









