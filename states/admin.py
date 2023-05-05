from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateCode(StatesGroup):
    text = State()


class SendCode(StatesGroup):
    text = State()
