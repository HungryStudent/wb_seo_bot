from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery
from aiogram.dispatcher import FSMContext

import keyboards.admin as admin_kb
import states.admin as states
from create_bot import dp
from config import ADMINS
from utils import db


@dp.message_handler(is_admin=True, content_types="video")
async def send_file_id_from_video(message: Message):
    await message.answer(message.video.file_id)


@dp.message_handler(is_admin=True, content_types="document")
async def send_file_id_from_document(message: Message):
    await message.answer(message.document.file_id)
