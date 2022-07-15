from aiogram import types
import json
from handlers.users.check_profile_info import get_order_message
from handlers.users.yourself import get_quantity
from keyboards.inline.edit_adress import edit_address
from keyboards.inline.is_pay import is_pay
from loader import dp, bot
from aiogram.dispatcher import FSMContext
import requests

from states.state import Setting


@dp.callback_query_handler(text='del', state=Setting.choice_method)
async def set_address(call: types.CallbackQuery, state=FSMContext):
    cart_data = await state.get_data()
    await bot.edit_message_text(chat_id=call.message.chat.id,
                                message_id=call.message.message_id,
                                text='Введите адрес доставки \n Введите улицу:',
                                reply_markup='')
    await Setting.set_street.set()
    await state.update_data(cart=cart_data['cart'])


@dp.message_handler(state=Setting.set_street)
async def set_address(message: types.Message, state=FSMContext):
    shipping_street = message.text
    cart_data = await state.get_data()
    await message.answer(text='Введите номер дома (с корпусом):')
    await Setting.set_house.set()
    await state.update_data(cart=cart_data['cart'], shipping_street=shipping_street)


@dp.message_handler(state=Setting.set_house)
async def set_address(message: types.Message, state=FSMContext):
    shipping_house = message.text
    cart_data = await state.get_data()
    await message.answer(text='Введите номер квартиры:')
    await Setting.set_flat.set()
    await state.update_data(cart=cart_data['cart'],
                            shipping_street=cart_data["shipping_street"],
                            shipping_house=shipping_house)


@dp.message_handler(state=Setting.set_flat)
async def set_address(message: types.Message, state=FSMContext):
    shipping_flat = message.text
    cart_data = await state.get_data()
    message_text = f'''
Адрес доставки:
{cart_data['shipping_street']}, {cart_data["shipping_house"]}, кв. {shipping_flat}
'''
    await message.answer(text=message_text, reply_markup=edit_address)
    await Setting.check_address.set()
    await state.update_data(cart=cart_data['cart'],
                            shipping_street=cart_data["shipping_street"],
                            shipping_house=cart_data['shipping_house'],
                            shipping_flat=shipping_flat
                            )


@dp.callback_query_handler(state=Setting.check_address)
async def set_address(call: types.CallbackQuery, state=FSMContext):
    cart_data = await state.get_data()
    if call.data == 'good_address':
        await call.message.edit_text(text='Введите комментарий для курьера')
        await Setting.set_comment_courier.set()
        await state.update_data(cart=cart_data['cart'],
                                shipping_address=f'{cart_data["shipping_street"]}, д. {cart_data["shipping_house"]}, кв. {cart_data["shipping_flat"]}')
    elif call.data == 'edit_street':
        await call.message.edit_text(text='Введите улицу повторно')
        await Setting.edit_street.set()
        await state.update_data(cart=cart_data['cart'],
                                shipping_street=cart_data["shipping_street"],
                                shipping_house=cart_data['shipping_house'],
                                shipping_flat=cart_data['shipping_flat']
                                )
    elif call.data == 'edit_house':
        await call.message.edit_text(text='Введите номер дома повторно')
        await Setting.edit_house.set()
        await state.update_data(cart=cart_data['cart'],
                                shipping_street=cart_data["shipping_street"],
                                shipping_house=cart_data['shipping_house'],
                                shipping_flat=cart_data['shipping_flat']
                                )
    elif call.data == 'edit_flat':
        await call.message.edit_text(text='Введите номер квартиры повторно')
        await Setting.edit_flat.set()
        await state.update_data(cart=cart_data['cart'],
                                shipping_street=cart_data["shipping_street"],
                                shipping_house=cart_data['shipping_house'],
                                shipping_flat=cart_data['shipping_flat']
                                )


@dp.message_handler(state=Setting.edit_street)
async def set_address(message: types.Message, state=FSMContext):
    edited_street = message.text
    cart_data = await state.get_data()
    message_text = f'''
    Адрес доставки:
    {edited_street}, {cart_data["shipping_house"]}, кв. {cart_data['shipping_flat']}
    '''
    await message.answer(text=message_text, reply_markup=edit_address)
    await Setting.check_address.set()
    await state.update_data(cart=cart_data['cart'],
                            shipping_street=edited_street,
                            shipping_house=cart_data['shipping_house'],
                            shipping_flat=cart_data['shipping_flat']
                            )


@dp.message_handler(state=Setting.edit_house)
async def set_address(message: types.Message, state=FSMContext):
    edited_house = message.text
    cart_data = await state.get_data()
    message_text = f'''
    Адрес доставки:
    {cart_data["shipping_street"]}, {edited_house}, кв. {cart_data['shipping_flat']}
    '''
    await message.answer(text=message_text, reply_markup=edit_address)
    await Setting.check_address.set()
    await state.update_data(cart=cart_data['cart'],
                            shipping_street=cart_data["shipping_street"],
                            shipping_house=edited_house,
                            shipping_flat=cart_data['shipping_flat']
                            )


@dp.message_handler(state=Setting.edit_flat)
async def set_address(message: types.Message, state=FSMContext):
    edited_flat = message.text
    cart_data = await state.get_data()
    message_text = f'''
    Адрес доставки:
    {cart_data["shipping_street"]}, {cart_data["shipping_house"]}, кв. {edited_flat}
    '''
    await message.answer(text=message_text, reply_markup=edit_address)
    await Setting.check_address.set()
    await state.update_data(cart=cart_data['cart'],
                            shipping_street=cart_data["shipping_street"],
                            shipping_house=cart_data["shipping_house"],
                            shipping_flat=edited_flat
                            )


@dp.message_handler(state=Setting.set_comment_courier)
async def set_address(message: types.Message, state=FSMContext):
    comment = message.text
    product_data = await state.get_data()
    message_text = 'Продукты: \n'
    total = 0
    for i in product_data['cart']:
        total_weight = i['weight'].split()
        summ = int(i['price']) * int(i['quantity'])
        total += summ
        message_text += f"{i['title']} {int(i['quantity']) * int(total_weight[0])} {total_weight[1]} — ₽{summ} \n"
    message_text += f'Адрес доставки: {product_data["shipping_address"]}\n'
    message_text += f'Комментарий: {comment}'
    message_text += get_order_message(total)
    await message.answer(text=message_text)
    await state.update_data(comment=comment)
    await Setting.payment.set()

    body_add_order = {
        "customer_tg_id": message.from_user.id,
        "shipping_address": product_data['shipping_address'],
        "comment": comment,
        "delivery_required": True,
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
