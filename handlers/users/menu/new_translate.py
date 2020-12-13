import asyncpg
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery

from keyboards.default import menu
from keyboards.inline.callback_data import select_dictionary_callback, add_translate_callback
from loader import dp, db
from states import CreateNewTranslate


@dp.callback_query_handler(add_translate_callback.filter(is_selected='True'))
async def new_translate_callback(call: CallbackQuery):
    """Query for input word"""
    await call.answer()
    await call.message.delete()
    await call.message.answer("Напиши слово на английском", reply_markup=ReplyKeyboardRemove())
    await CreateNewTranslate.SetEnglishWord.set()


@dp.message_handler(Text("📌Новый перевод"))
async def new_translate(message: Message):
    """Query for input word"""
    await message.answer("Напиши слово на английском", reply_markup=ReplyKeyboardRemove())
    await CreateNewTranslate.SetEnglishWord.set()


@dp.message_handler(state=CreateNewTranslate.SetEnglishWord)
async def set_english_word(message: Message, state: FSMContext):
    """Query for input translate for word"""
    await state.update_data(english_word=message.text)
    await message.answer("Теперь введи перевод своего слова")
    await CreateNewTranslate.SetRussianWord.set()


@dp.message_handler(state=CreateNewTranslate.SetRussianWord)
async def set_translate(message: Message, state: FSMContext):
    await state.update_data(russian_word=message.text)
    data = await state.get_data()
    english_word = data.get("english_word")
    russian_word = data.get("russian_word")
    user_id = message.from_user.id

    try:
        ########################################################################
        #                        DATABASE Queries                              #
        current_dictionary = await db.select_current_dictionary(user_id)
        await db.add_translate(english_word, russian_word, current_dictionary)
        translate = await db.select_last_translate(current_dictionary)
        translate_id = translate[0]
        await db.set_learning_translate(current_dictionary, translate_id)
        ########################################################################
        await message.answer(f"Добавлен новый перевод:\n"
                             f"{english_word} - {russian_word}", reply_markup=menu)
        await state.finish()

    except asyncpg.exceptions.NotNullViolationError:
        select_dictionaries = await db.select_dictionaries(user_id)
        if len(select_dictionaries) > 0:
            """It raised when user delete current dictionary and try to add new translate"""
            show_dictionaries_keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text=item[2],
                        callback_data=select_dictionary_callback.new(
                            dictionary_id=item[0],
                            dictionary_name=item[2]))] for item in select_dictionaries]
            )  # Generation dictionaries into inline buttons
            await message.answer("Так как вы удалили свой текущий словарь, \n"
                                 "то вам придется выбрать новый текущий словарь",
                                 reply_markup=show_dictionaries_keyboard)  # Showing all user dictionaries for select
        else:
            """It raised when user delete all dictionaries and try to add new translate"""
            await message.answer("У вас нету словарей! Добавьте хоть один словарь.", reply_markup=menu)
            await state.finish()
    except:
        await message.answer("Упс, какая-то ошибка!\n ", reply_markup=menu)
        await state.finish()


@dp.callback_query_handler(select_dictionary_callback.filter(), state=CreateNewTranslate.SetRussianWord)
async def changing_dictionary(call: CallbackQuery, callback_data: dict, state: FSMContext):
    """Setting current dictionary from exception"""
    await call.message.delete()
    name_selected_dictionary = callback_data['dictionary_name']
    user_id = call.from_user.id
    id_selected_dictionary = int(callback_data['dictionary_id'])
    ########################################################################
    #                        DATABASE Queries                              #
    await db.set_current_dictionary(user_id, id_selected_dictionary)
    ########################################################################
    await call.answer(f"Выбран словарь '{name_selected_dictionary}'", cache_time=5)
    await call.message.answer("Теперь вы можете создать перевод!", reply_markup=menu)
    await state.finish()
