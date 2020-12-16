import asyncio

import asyncpg
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from keyboards.default import menu
from loader import dp, db
from states import Start
from utils.misc import rate_limit


@rate_limit(limit=5)  # Anti-spam
@dp.message_handler(Command("start"))
async def start(message: Message):
    """Introduction for user, adding user to database"""
    first_name = message.from_user.first_name
    full_name = message.from_user.full_name
    user_id = message.from_user.id
    username = message.from_user.username

    try:
        ########################################################################
        #                         DATABASE Query                               #
        await db.add_user(user_id, first_name, full_name, username)  # Adding user to database
        ########################################################################

        await message.answer(f"Привет, {message.from_user.first_name}😜 Я вижу ты здесь впервые!\n\n"
                             "Вот небольшая инструкция:\n"
                             "    1. Чтобы добавить перевод, сначала нужно создать словарь\n"
                             "    2. В словарь уже можно добавлять переводы\n"
                             "    3. Можно учить!\n\n"
                             "Чтобы понять полностью процесс, рекомендую заглянуть в настройки и посмотреть:\n"
                             "    - Рекомендации\n"
                             "    - Полная инструкция\n")
        await asyncio.sleep(5)
        await message.answer("Ладно, перейдем к делу ...")
        await asyncio.sleep(2)
        await message.answer("Для начала тебе нужно добавить свой первый словарь.\n"
                             "Давай я тебе помогу!")
        await asyncio.sleep(3)
        await message.answer("⬇Напиши название своего первого словаря⬇")

        await Start.SetDictionary.set()

    except asyncpg.exceptions.UniqueViolationError:
        """It raised when registered user try to click /start command"""
        await message.answer("Вы уже зарегистрированы!", reply_markup=menu)


@dp.message_handler(state=Start.SetDictionary)
async def set_dict_name(message: Message, state: FSMContext):
    """Fetching first user dictionary name"""
    await state.update_data(dict_name=message.text)
    await message.answer("Отлично! Теперь давай добавим первый перевод.")
    await asyncio.sleep(2)
    await message.answer("Сперва введи слово на английском")
    await Start.SetEnglishWord.set()


@dp.message_handler(state=Start.SetEnglishWord)
async def set_english_word(message: Message, state: FSMContext):
    """Fetching first word"""
    await state.update_data(english_word=message.text)
    await message.answer("Теперь введи перевод своего слова")
    await Start.SetRussianWord.set()


@dp.message_handler(state=Start.SetRussianWord)
async def set_russian_word(message: Message, state: FSMContext):
    """ Adding main info about user to database

    Fetching translate for inputted word. Adding first dictionary and first translate to database
    Setting current dictionary. Setting user parameters.
    """
    await state.update_data(russian_word=message.text)

    data = await state.get_data()
    dict_name = data.get("dict_name")
    english_word = data.get("english_word")
    russian_word = data.get("russian_word")
    user_id = message.from_user.id
    user_language = message.from_user.language_code

    ########################################################################
    #                        DATABASE Queries                              #
    await db.add_dictionary(user_id, dict_name)    # Adding first dictionary
    dictionary_id_for_start = await db.select_dictionary_id_for_start(user_id)
    await db.set_current_dictionary(user_id, dictionary_id_for_start)  # Setting current dictionary
    current_dictionary = await db.select_current_dictionary(user_id)
    await db.add_translate(english_word, russian_word, current_dictionary)  # Adding first translate to current dict
    translate = await db.select_last_translate(current_dictionary)
    translate_id = translate[0]
    await db.set_learning_translate(current_dictionary, translate_id)  # Setup translate for learning
    await db.set_user_parameters(user_id, False, user_language)  # Setup user parameters
    ########################################################################

    await message.answer(f"Итак, название вашего словаря: \"{dict_name}\"\n"
                         f"Перевод:\n{english_word} - {russian_word}")
    await asyncio.sleep(1)
    await message.answer("Теперь ты можешь сам управлять своим переводчиком!\n"
                         "Напиши /menu чтобы посмотреть список команд.", reply_markup=menu)
    await state.finish()
