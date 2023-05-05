from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery

import keyboards.user as user_kb
from config import BOTNAME, SUPPORT_BOTNAME
from create_bot import dp
from utils import db


@dp.callback_query_handler(text="ref_menu", state="*")
async def ref_menu(call: CallbackQuery, state: FSMContext):
    await state.finish()

    user_ref_stat = await db.get_user_ref_stat(call.from_user.id)

    await call.message.edit_text(f"""Рассказывай друзьям о нашем боте и получай 20% от каждой оплаты реферала.

Реферальная ссылка: <code>https://t.me/{BOTNAME}/start={call.from_user.id}</code>

Рефералов: {user_ref_stat['refs_count']}
Баланс: {user_ref_stat['ref_balance']} руб.""", reply_markup=user_kb.ref_menu)


@dp.callback_query_handler(Text(startswith="withdraw_ref_balance"))
async def withdraw_ref_balance(call: CallbackQuery):
    to_type = call.data.split(":")[1]
    user_ref_stat = await db.get_user_ref_stat(call.from_user.id)
    if user_ref_stat['ref_balance'] == 0:
        await call.message.edit_text(f"""Ваш баланс пока что 0₽, рекомендуйте нашего бота и получайте 20% от каждой оплаты вашего реферала.

Ваша реферальная ссылка: <code>https://t.me/{BOTNAME}/start={call.from_user.id}</code>""",
                                     reply_markup=user_kb.back_to_menu)
        return
    if to_type == "balance":

        await db.remove_ref_balance(call.from_user.id)
        await db.add_balance(call.from_user.id, user_ref_stat['ref_balance'])

        user = await db.get_user(call.from_user.id)

        await call.message.edit_text(f"""{user_ref_stat['ref_balance']}₽ - зачислена на баланс бота
Баланс бота: {user['balance']}₽""", reply_markup=user_kb.back_to_menu)
    elif to_type == "card":
        await call.message.edit_text(f"Для вывода партнерского вознаграждения напишите нам @{SUPPORT_BOTNAME}",
                                     reply_markup=user_kb.back_to_menu)


