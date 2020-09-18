from aiogram.dispatcher.filters.state import StatesGroup, State


class Start(StatesGroup):
    SetDictionary = State()
    SetEnglishWord = State()
    SetRussianWord = State()
