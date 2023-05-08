import os
import re

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

import keyboards.user as user_kb
from config import BOTNAME, SUPPORT_BOTNAME
from create_bot import dp
from utils import db, wb_api, seo_report, google_api
from states.user import SeoRequest, LeaveContacts


@dp.callback_query_handler(text="seo_core", state="*")
async def seo_core_menu(call: CallbackQuery, state: FSMContext):
    await state.finish()

    await call.message.edit_text("""Пришлите что-то одно на выбор: поисковый запрос, ссылку на товар или артикул.

Например: 
 • “Легинсы”
 • 122864482
 • https://www.wildberries.ru/catalog/122864482/detail.aspx

Бот долго тренировался и анализировал миллионы товаров на WB. Поэтому ему достаточно одного запроса или артикула, чтобы собрать вам максимально полное SEO ядро, со всеми основными запросами и смежными запросами, по которым пользователи ищут аналогичные товары на WB.""",
                                 reply_markup=user_kb.back_to_menu)

    await state.set_state(SeoRequest.request)


@dp.message_handler(state=SeoRequest.request)
async def enter_request(message: Message, state: FSMContext):
    user = await db.get_user(message.from_user.id)
    if user["tokens"] <= 0:
        await message.answer("У вас закончились токены", reply_markup=user_kb.tariff)
        return

    category_id = None
    if not re.search(r'https://www.wildberries.ru/catalog/\d*/detail.aspx', message.text) is None:
        article_id = int(re.findall(r'https://www.wildberries.ru/catalog/(\d*)/detail.aspx', message.text)[0])
        card = await wb_api.get_card_details(article_id)
        if card is not None:
            category_id = card["subjectId"]
    elif message.text.isdigit():
        card = await wb_api.get_card_details(int(message.text))
        if card is not None:
            category_id = card["subjectId"]
    else:
        ads_data = await wb_api.get_ads(message.text)
        if ads_data["prioritySubjects"] is not None:
            category_id = ads_data["prioritySubjects"][0]

    if category_id is None:
        await message.answer("""🥺 Извините, я вас не понял. Попробуйте еще раз.

Пришлите что-то одно на выбор: поисковый запрос, ссылку на товар или артикул.

Например: 
 • “Легинсы”
 • 122864482
 • https://www.wildberries.ru/catalog/122864482/detail.aspx

Бот долго тренировался и анализировал миллионы товаров на WB. Поэтому ему достаточно одного запроса или артикула, чтобы собрать вам максимально полное SEO ядро, со всеми основными запросами и смежными запросами, по которым пользователи ищут аналогичные товары на WB.""",
                             reply_markup=user_kb.back_to_menu)
        return

    msg = await message.answer("⏳ Ожидайте, формируем результат...")

    filename = await seo_report.create_report(message.from_user.id, category_id)
    if filename == "Error":
        await msg.edit_text("Произошла ошибка, повторите попытку позже", reply_markup=user_kb.back_to_menu)
        await state.finish()
        return

    await msg.edit_text("""✅ SEO ядро готово
    На основе полученных данных вы можете самостоятельно сгенерировать SEO описание через бота, либо обратитесь к нашим SEO специалистам, которые комплексно проработают вашу карточку по самой доступной цене.""",
                        reply_markup=user_kb.seo_complete)
    await message.answer_document(open(filename, "rb"))
    os.remove(filename)
    await db.remove_token(message.from_user.id)
    await state.finish()


@dp.callback_query_handler(text="leave_contacts")
async def leave_contacts(call: CallbackQuery, state: FSMContext):
    await call.message.answer("Пришлите телефонный номер", reply_markup=user_kb.phone)
    await state.set_state(LeaveContacts.phone)
    await call.answer()


@dp.message_handler(content_types="contact", state=LeaveContacts.phone)
async def enter_phone(message: Message, state: FSMContext):
    await state.update_data(phone=message.contact.phone_number)
    await message.answer("Как мы можем к вам обращаться?", reply_markup=ReplyKeyboardRemove())
    await state.set_state(LeaveContacts.name)


@dp.message_handler(state=LeaveContacts.name)
async def enter_name(message: Message, state: FSMContext):
    await state.update_data(name=message.text)
    data = await state.get_data()

    google_api.add_lead(data["name"], data["phone"])

    await message.answer("""✅ ЗАЯВКА УСПЕШНО ПОЛУЧЕНА! 
Наш менеджер свяжется с вами в течении 5 минут, если заявка была оставлена в рабочее время.

Рабочее время с 10:00 до 20:00 по МСК""", reply_markup=user_kb.back_to_menu)
    await state.finish()
