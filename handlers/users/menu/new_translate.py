import asyncio
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ReplyKeyboardRemove, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
import asyncpg
from aiogram.dispatcher import FSMContext

from keyboards.inline.callback_data import select_dictionary_callback
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

    try:
        ########################################################################
        #                        DATABASE Queries                              #
        current_dictionary = await db.select_current_dictionary(tg_id)
        await db.add_translate(current_dictionary, english_word, russian_word)
        #                                                                      #
        ########################################################################
        await message.answer(f"Добавлен новый перевод:\n"
                             f"{english_word} - {russian_word}", reply_markup=menu)
        await state.finish()

    except asyncpg.exceptions.NotNullViolationError:
        select_dictionaries = await db.select_dictionaries(tg_id)
        if len(select_dictionaries) > 0:
            show_dictionaries_keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text=item[2],
                        callback_data=select_dictionary_callback.new(
                            dictionary_id=item[0],
                            dictionary_name=item[2]))] for item in select_dictionaries]
            )
            await message.answer("Так как вы удалили свой текущий словарь, \n"
                                 "то вам прийдется выбрать новый текущий словарь",
                                 reply_markup=show_dictionaries_keyboard)
        else:
            await message.answer("У вас нету словарей! Добавьте хоть один словарь.", reply_markup=menu)
            await state.finish()
    except:
        await message.answer(f"Упс, какая-то ошибка!", reply_markup=menu)
        await state.finish()


@dp.callback_query_handler(select_dictionary_callback.filter(), state=CreateNewTranslate.SetRussianWord)
async def changing_dictionary(call: CallbackQuery, callback_data: dict, state: FSMContext):
    name_selected_dictionary = callback_data['dictionary_name']
    tg_id = call.from_user.id
    id_selected_dictionary = int(callback_data['dictionary_id'])

    ########################################################################
    #                        DATABASE Queries                              #
    await db.set_current_dictionary(tg_id, id_selected_dictionary)
    ########################################################################
    await call.answer(f"Выбран словарь '{name_selected_dictionary}'", cache_time=5)
    await call.message.delete()

    await call.message.answer(f"Теперь вы можете создать перевод!", reply_markup=menu)

    await state.finish()
