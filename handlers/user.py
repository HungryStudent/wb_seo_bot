from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

import keyboards.user as user_kb
from create_bot import dp
from utils import db


@dp.message_handler(text="⏪ Главное меню", state="*")
@dp.message_handler(commands=['start'], state="*")
async def start_command(message: Message, state: FSMContext):
    await state.finish()
    user = await db.get_user(message.from_user.id)
    if user is None:
        try:
            inviter_id = int(message.get_args())
        except ValueError:
            inviter_id = None

        if inviter_id == message.from_user.id:
            inviter_id = None

        await db.add_user(message.from_user.id, message.from_user.username, message.from_user.first_name, inviter_id)

    await message.answer("""Приветствие""", reply_markup=user_kb.menu)


@dp.callback_query_handler(text="back_to_menu", state="*")
async def back_to_menu(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.edit_text("""Приветствие""", reply_markup=user_kb.menu)


@dp.callback_query_handler(text="back_to_menu_from_training", state="*")
async def back_to_menu(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer("Приветствие", reply_markup=user_kb.menu)


@dp.message_handler(state="*", text="Отмена")
async def cancel(message: Message, state: FSMContext):
    await state.finish()
    await message.answer("Ввод отменен", reply_markup=user_kb.menu)
