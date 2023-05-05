from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery
from aiogram import exceptions as tg_exceptions

from states.user import BrandState
import keyboards.user as user_kb
from create_bot import dp
from utils import db, chatgpt
from utils.chatgpt import brand_lang, brand_characters, brand_words_count


@dp.callback_query_handler(text="brand_generate", state="*")
async def brand_generate(call: CallbackQuery, state: FSMContext):
    await state.finish()

    await call.message.edit_text(f"""Пришлите название категории товара.
Например: Товары для дома""", reply_markup=user_kb.back_to_menu)
    await state.set_state(BrandState.category)


@dp.message_handler(state=BrandState.category)
async def enter_category(message: Message, state: FSMContext):
    await state.update_data(category=message.text)

    user = await db.get_user(message.from_user.id)

    await message.answer("""Выберите необходимые параметры
✅ - выбрано""", reply_markup=user_kb.get_brand(user))


@dp.callback_query_handler(Text(startswith="change_brand"), state=BrandState.category)
async def change_brand(call: CallbackQuery):
    changed_param = call.data.split(":")[1]
    value = int(call.data.split(":")[2])

    if changed_param == "lang":
        await db.change_brand_lang(call.from_user.id, value)
    elif changed_param == "characters":
        await db.change_brand_characters(call.from_user.id, value)
    elif changed_param == "words_count":
        await db.change_brand_words_count(call.from_user.id, value)
    user = await db.get_user(call.from_user.id)

    try:
        await call.message.edit_text("""Выберите необходимые параметры
✅ - выбрано""", reply_markup=user_kb.get_brand(user))
    except tg_exceptions.MessageNotModified:
        await call.answer()


@dp.callback_query_handler(text="start_brand_generate", state=BrandState.category)
async def start_brand_generate(call: CallbackQuery, state: FSMContext):
    data = await state.get_data()
    category = data["category"]
    user = await db.get_user(call.from_user.id)
    if user["tokens"] <= 0:
        await call.message.edit_text("У вас закончились токены", reply_markup=user_kb.tariff)
        return
    await call.message.edit_text("⏳ Ожидайте, формируем результат...")
    prompt = f"Нужно придумать название для бренда на {brand_lang[user['brand_lang_id']]['prompt']}. Название должно " \
             f"состоять из {brand_words_count[user['brand_words_count_id']]['prompt']}. Длина " \
             f"названия {brand_characters[user['brand_characters_id']]['prompt']}. Из названия бренда должна быть " \
             f"сразу понятна его основная функция. Предложи 10 вариантов. Бренд продает {category.lower()}."
    brands = await chatgpt.get_ans(prompt)
    await call.message.edit_text(
        f'Вот что получилось:\n{brands}\n\n<a href="https://onlinepatent.ru/?utm_source=partners&utm_medium=cpl&utm_content=13802"><u>Проверить доступность</u></a>',
        disable_web_page_preview=True, reply_markup=user_kb.get_brand_complete())
    await db.remove_token(call.from_user.id)
