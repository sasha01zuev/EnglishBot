from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateNewDict(StatesGroup):
    SetDictionaryName = State()

