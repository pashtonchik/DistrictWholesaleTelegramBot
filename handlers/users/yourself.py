import json
import requests

from aiogram import types
from handlers.users.check_profile_info import get_order_message
from keyboards.inline.is_pay import is_pay
from loader import dp, bot
from aiogram.dispatcher import FSMContext
from states.state import Setting


def get_quantity(item):
    weight = item['weight']
    quantity = item['quantity']
    quantity = quantity * 100 if weight[len(weight) - 2:] == 'ГР' else quantity
    return quantity


@dp.callback_query_handler(text='yourself', state=Setting.choice_method)
async def set_address(call: types.CallbackQuery, state=FSMContext):
    cart_data = await state.get_data()
    await bot.edit_message_text(chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                text='Введите комментарий для самовывоза:',
                                reply_markup='')
    await Setting.set_comment_yourself.set()
    await state.update_data(cart=cart_data['cart'])


@dp.message_handler(state=Setting.set_comment_yourself)
async def set_address(message: types.Message, state=FSMContext):
    comment = message.text
    product_data = await state.get_data()
    message_text = 'Продукты: \n'
    total = 0
    client_info = requests.get(f'https://onetwosneaker.ru/api2/customers/?tg_id={message.from_user.id}')
    client_discount = json.loads(client_info.text)[0]['discount']
    for i in product_data['cart']:
        total_weight = i['weight'].split()
        summ = int(i['price']) * int(i['quantity'])
        total += summ * ((100 - client_discount) / 100)
        message_text += f"{i['title']} {int(i['quantity']) * int(total_weight[0])} {total_weight[1]} — ₽{summ} \n"
    message_text += f'Комментарий: {comment}'
    message_text += get_order_message(total)
    await message.answer(text=message_text, reply_markup=is_pay)
    await state.update_data(comment=comment)
    await Setting.payment.set()
    body_add_order = {
        "customer_tg_id": message.from_user.id,
        "shipping_address": 'Самовывоз',
        "comment": comment,
        "delivery_required": False,
        "order_items": [
            {
                "vegetable_id": item['id'],
                "quantity": get_quantity(item),
            }
            for item in product_data['cart']
        ]
    }
    body_add_order = json.dumps(body_add_order)
    r = requests.post("https://onetwosneaker.ru/api2/addorder", data=body_add_order)
