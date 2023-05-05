from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

menu = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(KeyboardButton("Купить промокод"),
                                                                  KeyboardButton("Админка"),
                                                                  KeyboardButton("Техническая поддержка"))

cancel = ReplyKeyboardMarkup(resize_keyboard=True, row_width=1).add(KeyboardButton("Отмена"))

back_to_menu = InlineKeyboardMarkup(row_width=1).add(
    InlineKeyboardButton("В меню", callback_data="back_to_admin_select_category"))


def get_categories(categories):
    kb = InlineKeyboardMarkup(row_width=1)
    for category in categories:
        kb.add(InlineKeyboardButton(category['name'], callback_data=f'admin_select_category:{category["id"]}'))
    return kb


def get_products(products):
    kb = InlineKeyboardMarkup(row_width=1)
    for product in products:
        kb.add(InlineKeyboardButton(f"{product['count_months']} - {product['price']}",
                                    callback_data=f'admin_select_product:{product["id"]}'))
    kb.add(InlineKeyboardButton('Назад', callback_data='back_to_admin_select_category'))
    return kb


def get_codes(codes, category_id, product_id):
    kb = InlineKeyboardMarkup(row_width=1)
    for code in codes:
        if code["is_used"]:
            active_emoji = "🔴"
        else:
            active_emoji = "🟢"
        kb.add(InlineKeyboardButton(f"{active_emoji} {code['content']}",
                                    callback_data=f'admin_select_code:{code["id"]}'))
    kb.add(InlineKeyboardButton('Добавить', callback_data=f'add_code:{product_id}'))
    kb.add(InlineKeyboardButton('Назад', callback_data=f'back_to_admin_select_product:{category_id}'))
    return kb


def get_code(code_id, product_id):
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("Удалить", callback_data=f"delete_code:{code_id}"),
        InlineKeyboardButton("Назад", callback_data=f"back_to_codes:{product_id}"))


def get_send_code(order_id):
    return InlineKeyboardMarkup(row_width=1).add(
        InlineKeyboardButton("Отправить код", callback_data=f"send_code:{order_id}")
    )
