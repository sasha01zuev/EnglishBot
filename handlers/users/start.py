import asyncio

from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from loader import dp, bot, db
from states.start_for_new_user import Start
from keyboards.default import menu
from utils.misc import rate_limit
from datetime import datetime
import asyncpg

#for admin
from data.config import MAIN_ADMIN


@rate_limit(limit=5)
@dp.message_handler(Command("start"))
async def show_menu(message: Message):
    first_name = message.from_user.first_name
    full_name = message.from_user.full_name
    tg_id = message.from_user.id
    current_time = datetime.now()

    try:
        await db.add_user(tg_id, first_name, full_name, current_time, current_time)
        await message.answer(f"Привет, {message.from_user.first_name}! Я вижу ты здесь впервые!\n"
                             "Tы можешь прочитать в описании зачем я exist.\n"
                             "Кстати exist - существовать\n")
        await asyncio.sleep(5)
        await message.answer("Ладно, перейдем к делу ...")
        await asyncio.sleep(3)
        await message.answer("Для начала тебе нужно добавить свой первый словарь.\n"
                             "Давай я тебе помогу!")
        await asyncio.sleep(4.5)
        await message.answer("Напиши название своего словаря.\n"
                             "По умолчанию - Dictionary 1")

        await Start.SetDictionary.set()

    except asyncpg.exceptions.UniqueViolationError:
        await message.answer("Вы уже зарегистрированы!", reply_markup=menu)


@dp.message_handler(state=Start.SetDictionary)
async def set_dict_name(message: Message, state: FSMContext):
    await state.update_data(dict_name=message.text)
    await message.answer("Отлично! Теперь давай добавим первый перевод.")
    await asyncio.sleep(2)
    await message.answer("Сперва введи слово на английском")
    await Start.SetEnglishWord.set()


@dp.message_handler(state=Start.SetEnglishWord)
async def set_english_word(message: Message, state: FSMContext):
    await state.update_data(english_word=message.text)
    await message.answer("Теперь введи перевод своего слова")
    await Start.SetRussianWord.set()


@dp.message_handler(state=Start.SetRussianWord)
async def set_russian_word(message: Message, state: FSMContext):
    await state.update_data(russian_word=message.text)

    data = await state.get_data()
    dict_name = data.get("dict_name")
    english_word = data.get("english_word")
    russian_word = data.get("russian_word")
    tg_id = message.from_user.id

    ########################################################################
    #                        DATABASE Queries                              #
    await db.add_dictionary(tg_id, dict_name)
    dictionary_for_start = await db.select_dictionary_for_start(tg_id)
    await db.set_current_dictionary(tg_id, dictionary_for_start)
    current_dictionary = await db.select_current_dictionary(tg_id)
    await db.add_translate(current_dictionary, english_word, russian_word)
    await db.set_user_parameters(tg_id, False)
    ########################################################################

    await message.answer(f"Итак, название вашего словаря: \"{dict_name}\"\n"
                         f"Перевод:\n{english_word} - {russian_word}")

    await asyncio.sleep(1)
    await message.answer("Теперь ты можешь сам управлять своим переводчиком!\n"
                         "Напиши /menu чтобы посмотреть список команд.", reply_markup=menu)

    await state.finish()

    if str(message.from_user.id) != str(MAIN_ADMIN):
        await bot.send_message(MAIN_ADMIN, text=f"{message.from_user.first_name} "
                                                f"{message.from_user.last_name} "
                                                f"{message.from_user.id}:\n"
                                                f"Название словаря - {dict_name}\n"
                                                f"Перевод: {english_word} - {russian_word}")

