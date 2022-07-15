import json
import requests

from aiogram import types
from handlers.users.check_profile_info import get_order_message
from keyboards.inline.is_pay import is_pay
from loader import dp, bot
from aiogram.dispatcher import FSMContext
from states.state import Setting


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
    print(product_data['cart'])
    message_text = 'Продукты: \n'
    total = 0
    for i in product_data['cart']:
        summ = int(i['price']) * int(i['quantity'])
        total += summ
        message_text += f"{i['title']} x{i['quantity']} {i['weight']} — ₽{summ} \n"
    message_text += f'Комментарий курьеру: {comment}'
    message_text += get_order_message(total)
    await message.answer(text=message_text, reply_markup=is_pay)
    await Setting.payment.set()

    body_add_order = {
        "customer_tg_id": message.from_user.id,
        "shipping_address": 'Самовывоз',
        "comment": comment,
        "delivery_required": 0,
        "order_items": [
            {
                "vegetable_id": item['id'],
                "quantity": item['quantity'],
            }
            for item in product_data['cart']
        ]
    }
    print(body_add_order)
    body_add_order = json.dumps(body_add_order)
    r = requests.post("https://onetwosneaker.ru/api2/addorder", data=body_add_order)
