from datetime import datetime
import time

import asyncpg
from asyncpg import Connection
from asyncpg.exceptions import *
from config import DB


async def get_conn() -> Connection:
    return await asyncpg.connect(user=DB.user, password=DB.password, database=DB.database, host=DB.host)


async def start():
    conn: Connection = await get_conn()
    await conn.execute("CREATE TABLE IF NOT EXISTS users("
                       "user_id BIGINT PRIMARY KEY,"
                       "username VARCHAR(32),"
                       "firstname VARCHAR(64),"
                       "balance INT DEFAULT 0,"
                       "ref_balance INT DEFAULT 0,"
                       "inviter_id BIGINT REFERENCES users (user_id),"
                       "tokens SMALLINT DEFAULT 20,"
                       "desc_style_id SMALLINT DEFAULT 1,"
                       "brand_lang_id SMALLINT DEFAULT 1,"
                       "brand_characters_id SMALLINT DEFAULT 1,"
                       "brand_words_count_id SMALLINT DEFAULT 1)")

    await conn.execute("CREATE TABLE IF NOT EXISTS orders("
                       "order_id SERIAL PRIMARY KEY,"
                       "user_id BIGINT REFERENCES users (user_id),"
                       "tokens SMALLINT,"
                       "amount SMALLINT,"
                       "is_payd BOOL DEFAULT FALSE)")

    await conn.execute("CREATE TABLE IF NOT EXISTS category("
                       "category_id SMALLINT PRIMARY KEY,"
                       "category_name VARCHAR(256))")

    await conn.execute("CREATE TABLE IF NOT EXISTS search("
                       "search_id SERIAL PRIMARY KEY,"
                       "query VARCHAR(400) UNIQUE,"
                       "products_count INTEGER,"
                       "is_need_check BOOL)")

    await conn.execute("CREATE TABLE IF NOT EXISTS search_frequency("
                       "search_id INTEGER REFERENCES search (search_id),"
                       "frequency INTEGER,"
                       "report_type VARCHAR(10),"
                       "update_day INTEGER)")

    await conn.execute("CREATE TABLE IF NOT EXISTS search_priorities("
                       "search_id INTEGER REFERENCES search (search_id),"
                       "priorities_pos INTEGER,"
                       "category_id INTEGER,"
                       "PRIMARY KEY(search_id, priorities_pos))")
    await conn.close()


async def add_user(user_id, username, firstname, inviter_id):
    conn: Connection = await get_conn()
    try:
        await conn.execute(
            "INSERT INTO users(user_id, username, firstname, inviter_id) VALUES ($1, $2, $3, $4)",
            user_id, username, firstname, inviter_id)
    except asyncpg.exceptions.ForeignKeyViolationError:
        await conn.execute(
            "INSERT INTO users(user_id, username, firstname) VALUES ($1, $2, $3)",
            user_id, username, firstname)
    await conn.close()


async def get_user(user_id):
    conn: Connection = await get_conn()
    row = await conn.fetchrow("SELECT * from users WHERE user_id = $1", user_id)
    await conn.close()
    return row


async def get_user_ref_stat(user_id):
    conn: Connection = await get_conn()
    row = await conn.fetchrow("SELECT (SELECT ref_balance FROM users WHERE user_id = $1) as ref_balance,"
                              "(SELECT COUNT(user_id) FROM users WHERE inviter_id = $1) as refs_count", user_id)
    await conn.close()
    return row


async def remove_ref_balance(user_id):
    conn: Connection = await get_conn()
    await conn.execute(
        "UPDATE users SET ref_balance = 0 WHERE user_id = $1",
        user_id)
    await conn.close()


async def add_balance(user_id, amount):
    conn: Connection = await get_conn()
    await conn.execute(
        "UPDATE users SET balance = balance + $2 WHERE user_id = $1",
        user_id, amount)
    await conn.close()


async def remove_token(user_id):
    conn: Connection = await get_conn()
    await conn.execute(
        "UPDATE users SET tokens = tokens - 1 WHERE user_id = $1",
        user_id)
    await conn.close()


async def change_brand_lang(user_id, lang_id):
    conn: Connection = await get_conn()
    await conn.execute(
        "UPDATE users SET brand_lang_id = $2 WHERE user_id = $1",
        user_id, lang_id)
    await conn.close()


async def change_brand_characters(user_id, characters_id):
    conn: Connection = await get_conn()
    await conn.execute(
        "UPDATE users SET brand_characters_id = $2 WHERE user_id = $1",
        user_id, characters_id)
    await conn.close()


async def change_brand_words_count(user_id, words_count_id):
    conn: Connection = await get_conn()
    await conn.execute(
        "UPDATE users SET brand_words_count_id = $2 WHERE user_id = $1",
        user_id, words_count_id)
    await conn.close()


async def change_desc_style(user_id, desc_style_id):
    conn: Connection = await get_conn()
    await conn.execute(
        "UPDATE users SET desc_style_id = $2 WHERE user_id = $1",
        user_id, desc_style_id)
    await conn.close()


async def add_search(search_query, products_count, is_need_check):
    conn: Connection = await get_conn()
    try:
        row = await conn.fetchrow(
            "INSERT INTO search(query, products_count, is_need_check) VALUES ($1, $2, $3) RETURNING search_id",
            search_query, products_count, is_need_check)
    except UniqueViolationError:
        await conn.execute("UPDATE search SET products_count = $1 WHERE query = $2", products_count, search_query)
        row = await conn.fetchrow("SELECT search_id FROM search WHERE query = $1", search_query)
    await conn.close()
    return row["search_id"]


async def add_search_frequency(search_id, frequency, report_type, update_day):
    conn: Connection = await get_conn()
    await conn.execute(
        "INSERT INTO search_frequency(search_id, frequency, report_type, update_day) VALUES ($1, $2, $3, $4)",
        search_id, frequency, report_type, update_day)
    await conn.close()


async def delete_first_search_frequency():
    conn: Connection = await get_conn()
    row = await conn.fetchrow("SELECT COUNT(distinct update_day) as days_count FROM search_frequency")
    if row["days_count"] > 2:
        await conn.execute(
            "DELETE from search_frequency WHERE update_day = (SELECT MIN(update_day) FROM search_frequency)")
    await conn.close()


async def delete_search_priorities():
    conn: Connection = await get_conn()
    await conn.execute(
        "DELETE from search_priorities")
    await conn.close()


async def add_categories(categories):
    conn: Connection = await get_conn()
    await conn.executemany(
        "INSERT INTO category VALUES ($1, $2)",
        categories)
    await conn.close()


async def add_search_priorities(search_priorities):
    conn: Connection = await get_conn()
    await conn.executemany(
        "INSERT INTO search_priorities VALUES ($1, $2, $3)",
        search_priorities)
    await conn.close()


async def add_order(user_id, tokens, amount):
    conn: Connection = await get_conn()
    row = await conn.fetchrow(
        "INSERT INTO orders(user_id, tokens, amount) VALUES ($1, $2, $3) RETURNING order_id",
        user_id, tokens, amount)
    await conn.close()
    return row


async def get_order(order_id):
    conn: Connection = await get_conn()
    row = await conn.fetchrow("SELECT * from orders WHERE order_id = $1", order_id)
    await conn.close()
    return row


async def set_order_is_payd(order_id):
    conn: Connection = await get_conn()
    await conn.execute(
        "UPDATE orders SET is_payd = TRUE WHERE order_id = $1",
        order_id)
    await conn.close()


async def add_tokens(user_id, tokens):
    conn: Connection = await get_conn()
    await conn.execute(
        "UPDATE users SET tokens = tokens + $2 WHERE order_id = $1",
        user_id, tokens)
    await conn.close()


async def get_category_by_name(category_name):
    conn: Connection = await get_conn()
    row = await conn.fetchrow("SELECT category_id FROM category WHERE LOWER(category_name) = LOWER($1)", category_name)
    await conn.close()
    return row


async def get_search_by_report_type(report_type):
    conn: Connection = await get_conn()
    rows = await conn.fetch("""SELECT search.search_id,
       query,
       sf.frequency as frequency_1,
       sf1.frequency as frequency_2,
       products_count,
       is_need_check,
       sp1.category_id as category_id_1,
       sp2.category_id as category_id_2,
       sp3.category_id as category_id_3,
       sp4.category_id as category_id_4,
       sp5.category_id as category_id_5
FROM search
         join search_frequency sf on search.search_id = sf.search_id and sf.report_type = $1 and
                                     sf.update_day = (SELECT MIN(update_day) FROM search_frequency)
         left join search_frequency sf1 on search.search_id = sf1.search_id and sf1.report_type = $1 and
                                           sf1.update_day = (SELECT MAX(update_day) FROM search_frequency)
         left join search_priorities sp1 on search.search_id = sp1.search_id and sp1.priorities_pos = 1
         left join search_priorities sp2 on search.search_id = sp2.search_id and sp2.priorities_pos = 2
         left join search_priorities sp3 on search.search_id = sp3.search_id and sp3.priorities_pos = 3
         left join search_priorities sp4 on search.search_id = sp4.search_id and sp4.priorities_pos = 4
         left join search_priorities sp5 on search.search_id = sp5.search_id and sp5.priorities_pos = 5""", report_type)
    await conn.close()
    return rows


async def get_priorities_by_category_id(category_id):
    conn: Connection = await get_conn()
    rows = await conn.fetch("""SELECT search_priorities.search_id, s.query, sf.frequency, s.products_count,
    search_priorities.priorities_pos
FROM search_priorities
         join search s on s.search_id = search_priorities.search_id
         left join search_frequency sf on s.search_id = sf.search_id and sf.report_type = 'month' and
                                           sf.update_day = (SELECT MAX(update_day) FROM search_frequency)
WHERE category_id = $1""",
                            category_id)
    await conn.close()
    return rows
