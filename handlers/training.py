from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

import keyboards.user as user_kb
from config import BOTNAME, SUPPORT_BOTNAME, video_file_id, doc_file_id
from create_bot import dp
from utils import db


@dp.callback_query_handler(text="training", state="*")
async def training(call: CallbackQuery, state: FSMContext):
    await state.finish()
    await call.message.answer_video(video_file_id)
    await call.message.answer_document(doc_file_id, reply_markup=user_kb.back_to_menu_from_training)
    await call.message.delete()
