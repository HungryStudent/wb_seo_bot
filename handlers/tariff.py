from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery, LabeledPrice, PreCheckoutQuery

import keyboards.user as user_kb
from config import BOTNAME, SUPPORT_BOTNAME, pay_token
from create_bot import dp
from utils import db


@dp.callback_query_handler(text="tariff", state="*")
async def tariff(call: CallbackQuery, state: FSMContext):
    await state.finish()

    user = await db.get_user(call.from_user.id)
    await call.message.edit_text(f"""Доступно генераций: {user['tokens']}
Сбор семантики / Генерация описания / Генерация 10 названий бренда - каждое из этих действий тратит 1 генерацию

20 шт - 290 ₽
50 шт - 590 ₽
100 шт - 990 ₽
200 шт - 1 490 ₽
500 шт - 2 990 ₽""", reply_markup=user_kb.tariff)


@dp.callback_query_handler(Text(startswith="buy_tokens"))
async def buy_tokens(call: CallbackQuery):
    tokens, amount = call.data.split(":")[1:]
    order_id = await db.add_order(call.from_user.id, tokens, amount)
    await call.bot.send_invoice(call.from_user.id, title="Покупка генераций",
                                description="Для оплаты тарифа перейдите по ссылке: Оплатить",
                                payload=order_id, provider_token=pay_token, currency="RUB",
                                prices=[LabeledPrice(label="Оплата аккаунта", amount=amount * 100)],
                                reply_markup=user_kb.back_to_menu_from_training)


@dp.pre_checkout_query_handler()
async def approve_order(pre_checkout_query: PreCheckoutQuery):
    await pre_checkout_query.bot.answer_pre_checkout_query(pre_checkout_query.id, ok=True)


@dp.message_handler(content_types="successful_payment")
async def process_successful_payment(message: Message):
    order = db.get_order(message.successful_payment.invoice_payload)
    await db.set_order_is_payd(order["id"])
    user = await db.get_user(order["user_id"])
    await db.add_tokens(user["user_id"], order["tokens"])
    await message.answer(f"Платеж проведен. На ваш аккаунт зачислено {order['tokens']} токенов")
