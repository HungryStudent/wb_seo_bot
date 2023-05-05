from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery
from aiogram import exceptions as tg_exceptions

from states.user import DescState
import keyboards.user as user_kb
from create_bot import dp
from utils import db, chatgpt
from utils.chatgpt import desc_style


@dp.callback_query_handler(text="desc_generate", state="*")
async def desc_generate(call: CallbackQuery, state: FSMContext):
    await state.finish()

    await call.message.edit_text(f"""🧐 Приступим, пришлите мне данные товара в формате:
1. Название товара
2. Ключевые слова и фразы (можно через запятую или каждый запрос с новой строки)

Например:
Зимняя куртка
утепленная, ветрозащитная, водонепроницаемая, стильная, функциональная, на молнии, с капюшоном, теплая, мужская, женская, детская.
⏪️ Главное меню""", reply_markup=user_kb.back_to_menu)
    await state.set_state(DescState.desc_data)


@dp.message_handler(state=DescState.desc_data)
async def enter_desc_data(message: Message, state: FSMContext):
    msg_data = message.text.split("\n")
    await state.update_data(name=msg_data[0])
    if len(msg_data) > 2:
        phrases = msg_data[1:]
    else:
        phrases = msg_data[1].replace(", ", ",")
        phrases = phrases.split(",")
    await state.update_data(phrases=phrases)

    user = await db.get_user(message.from_user.id)

    await message.answer("""Выберите стиль написания -это важный элемент, определяющий направление повествования. Каждый стиль имеет свои особенности и соответствует определенному типу товара и целевой аудитории. Правильный выбор стиля поможет создать эффективное описание товара, которое привлечет внимание и заинтересует потенциального покупателя. 
<a href="https://telegra.ph/Stili-03-23"><u>Подробнее о стилях</u></a>""", reply_markup=user_kb.get_desc(user),
                         disable_web_page_preview=True)


@dp.callback_query_handler(Text(startswith="change_desc"), state=DescState.desc_data)
async def change_desc(call: CallbackQuery):
    value = int(call.data.split(":")[1])

    await db.change_desc_style(call.from_user.id, value)
    user = await db.get_user(call.from_user.id)

    try:
        await call.message.edit_text("""Выберите стиль написания -это важный элемент, определяющий направление повествования. Каждый стиль имеет свои особенности и соответствует определенному типу товара и целевой аудитории. Правильный выбор стиля поможет создать эффективное описание товара, которое привлечет внимание и заинтересует потенциального покупателя. 
<a href="https://telegra.ph/Stili-03-23"><u>Подробнее о стилях</u></a>""", reply_markup=user_kb.get_desc(user),
                                     disable_web_page_preview=True)
    except tg_exceptions.MessageNotModified:
        await call.answer()


@dp.callback_query_handler(text="start_desc_generate", state=DescState.desc_data)
async def start_desc_generate(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    name = data["name"]
    phrases = data["phrases"]
    user = await db.get_user(call.from_user.id)
    if user["tokens"] <= 0:
        await call.message.edit_text("У вас закончились токены", reply_markup=user_kb.tariff)
        return
    await call.message.edit_text("⏳ Ожидайте, формируем результат...")
    prompt = f"Напиши описание для карточки товара длинной 2000 символов: {name}, используй все перечисленные ниже слова: {', '.join(phrases)}. Стиль написания {desc_style[user['desc_style_id']]['prompt']}"
    print(prompt)
    desc = await chatgpt.get_ans(prompt)
    await call.message.edit_text(
        f'Вот что получилось:\n\n{desc}', disable_web_page_preview=True, reply_markup=user_kb.get_desc_complete())
    await db.remove_token(call.from_user.id)
