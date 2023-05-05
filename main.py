from aiogram.utils import executor
from create_bot import dp
from utils import db
from handlers import __init__
from utils.chatgpt import get_ans


async def on_startup(_):
    await db.start()


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True, on_startup=on_startup)
