from aiogram.dispatcher.filters.state import StatesGroup, State


class CreateNewDict(StatesGroup):
    SetDictionaryName = State()


class CreateNewTranslate(StatesGroup):
    SetEnglishWord = State()
    SetRussianWord = State()


class DeleteLastDictionary(StatesGroup):
    SetDeleteDictionary = State()


class DeleteListDictionary(StatesGroup):
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


class ChangeDictionary(StatesGroup):
    SetChangeDictionary = State()


class SelectLanguage(StatesGroup):
    SetLanguage = State()


class StartLearningTranslates(StatesGroup):
    SetLearning = State()


class ChooseResponse(StatesGroup):
    SetChooseResponse = State()
