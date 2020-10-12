from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateNewDict(StatesGroup):
    SetDictionaryName = State()


class CreateNewTranslate(StatesGroup):
    SetEnglishWord = State()
    SetRussianWord = State()


class DeleteDictionary(StatesGroup):
    SetDeleteDictionary = State()


class DeleteInputtedTranslate(StatesGroup):
    InputWord = State()


class DeleteLastTranslate(StatesGroup):
    SetDeleteLastTranslate = State()


class DeleteTranslate(StatesGroup):
    SetDeleteTranslate = State()


class Start(StatesGroup):
    SetDictionary = State()
    SetEnglishWord = State()
    SetRussianWord = State()