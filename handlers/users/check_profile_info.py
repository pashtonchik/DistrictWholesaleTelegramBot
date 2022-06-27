from itertools import product
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.types import WebAppInfo, InlineKeyboardMarkup, InlineKeyboardButton, ContentType
from aiogram.dispatcher.filters.state import State, StatesGroup
from bd_custumers import take_customer, edit_customer, input_all
import data
from freekassa import create_link
from keyboards.inline.yesno import yesorno
from keyboards.inline.edit_profile import edit
from keyboards.inline.yesno import yesorno
import json
from loader import dp, bot
from states.state import setting
from aiogram.dispatcher import FSMContext
import requests
import datetime
PAYMENTS_PROVIDER_TOKEN = '390540012:LIVE:24861'


@dp.message_handler(content_types="web_app_data", state='*')
async def answer(webAppMes: types.WebAppData, state: FSMContext):
    data_json = json.loads(webAppMes.web_app_data.data)
    print(data_json)
    message = 'Кроссовки: '
    total = 0
    PRICE = []
    for i in data_json:
        summ = int(i['price']) * int(i['quantity'])
        total += summ
        message += f"{i['title']} x{i['quantity']} Размер: {i['size']} — ₽{summ}, "
        summ = 100
        PRICE.append(types.LabeledPrice(label=f"{i['title']}\n Размер: {i['size']} ", amount=summ * 100))
    message += f"Итоговая сумма: ₽{total}\n"
    types.LabeledPrice(label='Ваш заказ', amount=total * 100)
    total = 1000
    await state.finish()
    await state.update_data(product=data_json)
    await bot.send_invoice(
        webAppMes.chat.id,
        title='Оплата заказа',
        description=message,
        provider_token=PAYMENTS_PROVIDER_TOKEN,
        currency='rub',
        is_flexible=False,  # True если конечная цена зависит от способа доставки
        prices=PRICE,
        need_name=True,
        need_phone_number= True,
        send_phone_number_to_provider=True,
        need_shipping_address=True,
        start_parameter='time-machine-example',
        payload='some-invoice-payload-for-our-internal-use',
    )


@dp.pre_checkout_query_handler(lambda query: True)
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    print(pre_checkout_query)
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: types.Message, state: FSMContext):
    data = await state.get_data()
    await state.finish()
    sneaker = list()
    
    for i in data['product']:
        sneaker.append({'product_name' : i['title'], 'size' : i['size'], 'quantity': i['quantity'], 'price': i['price']})
    pmnt = message.successful_payment.to_python()
    print(pmnt['order_info'])
    date = str(datetime.datetime.now().date())
    url = 'http://194.58.107.7:8000'
    req = f"""{url}/api/resource/Selling%20Order%20OneTwoSneaker"""
    jn = {"customer_name": pmnt['order_info']["name"],
        "date": date,
        "phone_number": pmnt['order_info']["phone_number"],
        "address1": pmnt['order_info']["shipping_address"]["street_line1"],
        "address2": pmnt['order_info']["shipping_address"]["street_line2"],
        "city": pmnt['order_info']["shipping_address"]["city"],
        "state": pmnt['order_info']["shipping_address"]["state"],
        "postcode": pmnt['order_info']["shipping_address"]["post_code"],
        "product" : sneaker
    }
    headers = {
    'Authorization': "token ed87374be6f1468:769aa1df0bae7f5",
    'Content-Type': 'application/json',
    'Accept': 'application/json'
    }
    data = json.dumps(jn)
    try:
        response = requests.post(url = req, data = data, headers=headers)
        if (response.status_code == 200):
            await bot.send_message(
                message.chat.id,
                'Оплата прошла успешно! С вами скоро свяжется наш менеджер!'
            )
        else:
            await bot.send_message(
                message.chat.id, 
                'Произошла ошибка, <b>свяжитесь</b> с тех. поддержкой! Наш ТГ: t.me/a5caff8b53cbd89e51822f1c3e0e66d2',
                parse_mode='HTML') 
    except Exception as e:
        await bot.send_message(message.chat.id, 'Произошла ошибка, <b>свяжитесь</b> с тех. поддержкой! Наш ТГ: t.me/a5caff8b53cbd89e51822f1c3e0e66d2',
             parse_mode='HTML') 