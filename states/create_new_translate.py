from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateNewTranslate(StatesGroup):
    SetEnglishWord = State()
    SetRussianWord = State()

