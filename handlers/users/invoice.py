from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton

from bd_custumers import insert_customer, input_all
from keyboards.inline.yesno import yesorno

from loader import dp, bot
from states.state import setting

PAYMENTS_PROVIDER_TOKEN = '381764678:TEST:38820'
PRICE = types.LabeledPrice(label='Настоящая Машина Времени', amount=4200000)


@dp.message_handler(commands=['buy'], state='*')
async def process_buy_command(message: types.Message):
    if PAYMENTS_PROVIDER_TOKEN.split(':')[1] == 'TEST':
        await bot.send_message(message.chat.id, 'покупай')
        await bot.send_invoice(
            message.chat.id,
            title='бебра',
            description='вкусная',
            provider_token=PAYMENTS_PROVIDER_TOKEN,
            currency='rub',
            photo_height=512,  # !=0/None, иначе изображение не покажется
            photo_width=512,
            photo_size=512,
            is_flexible=False,  # True если конечная цена зависит от способа доставки
            prices=[PRICE],
            start_parameter='time-machine-example',
            payload='some-invoice-payload-for-our-internal-use'
        )