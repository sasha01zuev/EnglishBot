import asyncio
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ReplyKeyboardRemove
import asyncpg
from aiogram.dispatcher import FSMContext
from states.create_new_translate import CreateNewTranslate

from keyboards.default import menu
from loader import dp, db


@dp.message_handler(Text("Новый перевод"))
async def new_translate(message: Message):
    await message.answer("Напиши слово на английском", reply_markup=ReplyKeyboardRemove())
    await CreateNewTranslate.SetEnglishWord.set()


@dp.message_handler(state=CreateNewTranslate.SetEnglishWord)
async def set_english_word(message: Message, state: FSMContext):
    await state.update_data(english_word=message.text)
    await message.answer("Теперь введи перевод своего слова")
    await CreateNewTranslate.SetRussianWord.set()


@dp.message_handler(state=CreateNewTranslate.SetRussianWord)
async def set_russian_word(message: Message, state: FSMContext):
    await state.update_data(russian_word=message.text)
    data = await state.get_data()
    dict_name = data.get("dict_name")
    english_word = data.get("english_word")
    russian_word = data.get("russian_word")
    tg_id = message.from_user.id

    ########################################################################
    #                        DATABASE Queries                              #
    current_dictionary = await db.select_current_dictionary(tg_id)
    await db.add_translate(current_dictionary, english_word, russian_word)
    #                                                                      #
    ########################################################################
    await message.answer(f"Добавлен новый перевод:\n"
                         f"{english_word} - {russian_word}", reply_markup=menu)
    await state.finish()
