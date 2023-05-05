from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.utils.callback_data import CallbackData

from utils import chatgpt

menu = InlineKeyboardMarkup(resize_keyboard=True, row_width=1).add(
    InlineKeyboardButton("Собрать SEO ядро", callback_data="seo_core"),
    InlineKeyboardButton("Сгенерировать описание", callback_data="desc_generate"),
    InlineKeyboardButton("Название для бренда", callback_data="brand_generate"),
    InlineKeyboardButton("Обучение", callback_data="training"),
    InlineKeyboardButton("Тариф", callback_data="tariff"),
    InlineKeyboardButton("Заказать SEO под ключ", callback_data="buy_seo"),
    InlineKeyboardButton("Реферальная программа", callback_data="ref_menu"))

back_to_menu = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("⏪ Главное меню", callback_data="back_to_menu"))

back_to_menu_from_training = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("⏪ Главное меню", callback_data="back_to_menu_from_training"))

back_to_menu_from_pay = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("Оплатить", pay=True),
    InlineKeyboardButton("⏪ Главное меню", callback_data="back_to_menu_from_pay"))

cancel = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(KeyboardButton("Отмена"))

tariff = InlineKeyboardMarkup(row_width=2).add(
    InlineKeyboardButton("20 шт.", callback_data="buy_tokens:20:290"),
    InlineKeyboardButton("50 шт.", callback_data="buy_tokens:50:590"),
    InlineKeyboardButton("100 шт.", callback_data="buy_tokens:100:990"),
    InlineKeyboardButton("200 шт.", callback_data="buy_tokens:200:1490")).add(
    InlineKeyboardButton("500 шт.", callback_data="buy_tokens:500:2990")).add(
    InlineKeyboardButton("⏪ Главное меню", callback_data="back_to_menu"))

ref_menu = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("Зачислить на баланс", callback_data="withdraw_ref_balance:balance"),
    InlineKeyboardButton("Вывести на карту", callback_data="withdraw_ref_balance:card"),
    InlineKeyboardButton("⏪ Главное меню", callback_data="back_to_menu"))

seo_complete = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("Сделаю сам", callback_data="desc_generate", ),
    InlineKeyboardButton("Обращусь к вам", callback_data="leave_contacts"),
    InlineKeyboardButton("⏪ Главное меню", callback_data="back_to_menu")
)

phone = ReplyKeyboardMarkup(row_width=1, resize_keyboard=True).add(KeyboardButton("Отправить", request_contact=True),
                                                                   KeyboardButton("⏪ Главное меню"))


def get_brand(user):
    kb = InlineKeyboardMarkup(row_width=2)
    for index, lang in enumerate(chatgpt.brand_lang):
        if index == 0:
            continue
        btn_text = lang["name"]
        if index == user["brand_lang_id"]:
            btn_text = "✅" + lang["name"]
        kb.insert(InlineKeyboardButton(btn_text, callback_data=f"change_brand:lang:{index}"))

    for index, characters in enumerate(chatgpt.brand_characters):
        if index == 0:
            continue
        btn_text = characters["name"]
        if index == user["brand_characters_id"]:
            btn_text = "✅" + characters["name"]
        kb.insert(InlineKeyboardButton(btn_text, callback_data=f"change_brand:characters:{index}"))

    for index, words_count in enumerate(chatgpt.brand_words_count):
        if index == 0:
            continue
        btn_text = words_count["name"]
        if index == user["brand_words_count_id"]:
            btn_text = "✅" + words_count["name"]
        kb.insert(InlineKeyboardButton(btn_text, callback_data=f"change_brand:words_count:{index}"))

    kb.add(InlineKeyboardButton("Запустить", callback_data="start_brand_generate"))
    kb.add(InlineKeyboardButton("⏪ Главное меню", callback_data="back_to_menu"))

    return kb


def get_brand_complete():
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("🔄 Ещё варианты", callback_data="start_brand_generate"),
        InlineKeyboardButton("⏪ Главное меню", callback_data="back_to_menu"))


def get_desc(user):
    kb = InlineKeyboardMarkup(row_width=2)
    for index, style in enumerate(chatgpt.desc_style):
        if index == 0:
            continue
        btn_text = style["name"]
        if index == user["desc_style_id"]:
            btn_text = "✅" + style["name"]
        if index == 6:
            kb.add(InlineKeyboardButton(btn_text, callback_data=f"change_desc:{index}"))
        else:
            kb.insert(InlineKeyboardButton(btn_text, callback_data=f"change_desc:{index}"))

    kb.add(InlineKeyboardButton("Запустить", callback_data="start_desc_generate"))
    kb.add(InlineKeyboardButton("⏪ Главное меню", callback_data="back_to_menu"))

    return kb


def get_desc_complete():
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("🔄 Ещё варианты", callback_data="start_desc_generate"),
        InlineKeyboardButton("⏪ Главное меню", callback_data="back_to_menu"))
