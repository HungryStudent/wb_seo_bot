from aiogram.dispatcher.filters.state import StatesGroup, State


class BrandState(StatesGroup):
    category = State()


class DescState(StatesGroup):
    desc_data = State()


class SeoRequest(StatesGroup):
    request = State()


class LeaveContacts(StatesGroup):
    phone = State()
    name = State()