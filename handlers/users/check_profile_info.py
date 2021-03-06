from aiogram import types
import json

from data import config
from keyboards.inline.delivery import delivery
from loader import dp, bot
from aiogram.dispatcher import FSMContext
import requests

from states.state import Setting


def get_order_message(total_cost, discount):
    if discount:
        return f"""\n
Итоговая сумма с учетом скидки: ₽{total_cost}\n
<u>Для оплаты заказа переведите <b>{total_cost}</b>₽ по этому номеру карты </u> \n
<code> {config.CART_NUMBER} </code>
\n
После отправки средств, нажмите кнопку "Оплатил"
"""

    else:
        return f"""\n
Итоговая сумма: ₽{total_cost}\n
<u>Для оплаты заказа переведите <b>{total_cost}</b>₽ по этому номеру карты </u> \n
<code> {config.CART_NUMBER} </code>
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
            total_weight = i['weight'].split()

            summ = int(i['price']) * int(i['quantity'])
            total += summ
            message += f"{i['title']} {int(i['quantity']) * int(total_weight[0])} {total_weight[1]} — ₽{summ} \n"

        await bot.send_message(webappmes.chat.id, message, reply_markup=delivery)
        await Setting.choice_method.set()
        await state.update_data(cart=data_json)
    else:
        await webappmes.answer(text='Сервер в данный момент недоступен, повторите попытку позже')
        await state.finish()


@dp.callback_query_handler(state=Setting.payment)
async def process_successful_payment(call: types.CallbackQuery, state: FSMContext):
    if call.data == 'is_paid':
        product_data = await state.get_data()
        message_text = product_data['message_text']
        await call.message.edit_text(message_text)
        await call.message.answer('Спасибо! Отправьте чек об оплате менеджеру - @LarS2S')
        await state.finish()
    elif call.data == 'cancel':
        await call.message.edit_text('Можете продолжить покупки, нажав на кнопку "Заказать продукты"', reply_markup='')
        await state.finish()
