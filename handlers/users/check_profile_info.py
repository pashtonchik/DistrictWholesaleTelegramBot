from aiogram import types
from aiogram.types import ContentType, InlineKeyboardButton, InlineKeyboardMarkup
import json

from keyboards.inline.delivery import delivery
from keyboards.inline.is_pay import is_pay
from keyboards.inline.no_comments import no_comments
from keyboards.inline.yesno import yesorno
from loader import dp, bot
from aiogram.dispatcher import FSMContext
import requests

from states.state import Setting

PAYMENTS_PROVIDER_TOKEN = '381764678:TEST:38490'


def get_order_message(total_cost):
    return \
        f"""\n
Итоговая сумма: ₽{total_cost}\n
<u>Для оплаты заказа переведите <b>{total_cost}</b>₽ по этому номеру карты </u> \n
<code> 4242424242424242 </code>
\n
После отправки средств, нажмите кнопку "Оплатил"
"""


@dp.message_handler(content_types="web_app_data", state='*')
async def answer(webappmes: types.WebAppData, state: FSMContext):
    user_data = await state.get_data()
    check_request = requests.get('https://onetwosneaker.ru/api/check')
    if check_request.status_code == 200:
        data_json = json.loads(webappmes.web_app_data.data)
        message = 'Продукты: \n'
        total = 0
        for i in data_json:
            summ = int(i['price']) * int(i['quantity'])
            total += summ
            message += f"{i['title']} x{i['quantity']} {i['weight']} — ₽{summ} \n"

        await bot.send_message(webappmes.chat.id, message, reply_markup=delivery)
        await Setting.choice_method.set()
        await state.update_data(cart=data_json)
    else:
        await webappmes.answer(text='Сервер в данный момент недоступен, повторите попытку позже')
        await state.finish()


@dp.callback_query_handler(state=Setting.payment)
async def process_successful_payment(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'is_paid':
        await call.message.answer('Спасибо! Отправьте чек об оплате менеджеру - @LarS2S')
        await state.finish()
    elif call.data == 'cancel':
        await call.message.edit_text('Можете продолжить покупки, нажав на кнопку "Заказать продукты"', reply_markup='')
        await state.finish()