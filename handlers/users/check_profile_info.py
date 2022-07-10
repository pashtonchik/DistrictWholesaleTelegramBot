from aiogram import types
from aiogram.types import ContentType
import json
from loader import dp, bot
from aiogram.dispatcher import FSMContext
import requests

PAYMENTS_PROVIDER_TOKEN = '381764678:TEST:38490'


@dp.message_handler(content_types="web_app_data", state='*')
async def answer(webAppMes: types.WebAppData, state: FSMContext):
    check_request = requests.get('https://onetwosneaker.ru/api/check')
    if check_request.status_code == 200:
        data_json = json.loads(webAppMes.web_app_data.data)
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
            need_phone_number=True,
            send_phone_number_to_provider=True,
            need_shipping_address=True,
            start_parameter='time-machine-example',
            payload='some-invoice-payload-for-our-internal-use',
        )
    else:
        await webAppMes.answer(text='Сервер в данный момент недоступен, повторите попытку позже')
        await state.finish()


@dp.pre_checkout_query_handler(lambda query: True)
async def process_pre_checkout_query(pre_checkout_query: types.PreCheckoutQuery):
    await bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types=ContentType.SUCCESSFUL_PAYMENT)
async def process_successful_payment(message: types.Message, state: FSMContext):
    sneakers_data = await state.get_data()
    await state.finish()
    pmnt = message.successful_payment.to_python()['order_info']
    body = {
        'order_list': {
            "customer": pmnt['name'],
            "shipping_address": f'''{pmnt['shipping_address']['city']}, {pmnt['shipping_address']['street_line1']}, {pmnt['shipping_address']['street_line2']} ''',
            "phone_number": pmnt['phone_number'],
        },
        'order_items': [
            {
                'sneaker_id': item['id'],
                'sneaker_size': item['size'],
                'quantity': item['quantity'],
            }
            for item in sneakers_data['product']
        ]
    }
    print(body)
    b = requests.post("https://onetwosneaker.ru/api/addorder", data=json.dumps(body))
    if b.status_code == 200:
        order_id = b.json()['order_id']
        await bot.send_message(message.chat.id, f'Оплата произошла успешно, номер вашего заказа {order_id}', parse_mode='HTML')
    else:
        await bot.send_message(message.chat.id,
                               'Произошла ошибка, <b>свяжитесь</b> с тех. поддержкой! Наш ТГ: t.me/a5caff8b53cbd89e51822f1c3e0e66d2',
                               parse_mode='HTML')
