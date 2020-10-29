import asyncio

from aiogram.dispatcher.filters import Command
from aiogram.dispatcher import FSMContext
from aiogram.types import Message

from loader import dp, db, _
from states import Start
from keyboards.default import menu
from utils.misc import rate_limit

import asyncpg


@rate_limit(limit=5)
@dp.message_handler(Command("start"))
async def show_menu(message: Message):
    first_name = message.from_user.first_name
    full_name = message.from_user.full_name
    tg_id = message.from_user.id
    username = message.from_user.username

    try:
        ########################################################################
        #                         DATABASE Query                               #
        await db.add_user(tg_id, first_name, full_name, username)
        ########################################################################

        await message.answer(_("Привет, {message}! Я вижу ты здесь впервые!\n"
                               "Tы можешь прочитать в описании зачем я exist.\n"
                               "Кстати exist - существовать\n").format(message=message.from_user.first_name))
        await asyncio.sleep(4)
        await message.answer(_("Ладно, перейдем к делу ..."))
        await asyncio.sleep(2)
        await message.answer(_("Для начала тебе нужно добавить свой первый словарь.\n"
                             "Давай я тебе помогу!"))
        await asyncio.sleep(3)
        await message.answer(_("Напиши название своего словаря.\n"
                             "По умолчанию - Dictionary 1"))

        await Start.SetDictionary.set()

    except asyncpg.exceptions.UniqueViolationError:
        await message.answer(_("Вы уже зарегистрированы!"), reply_markup=menu)


@dp.message_handler(state=Start.SetDictionary)
async def set_dict_name(message: Message, state: FSMContext):
    await state.update_data(dict_name=message.text)
    await message.answer(_("Отлично! Теперь давай добавим первый перевод."))
    await asyncio.sleep(2)
    await message.answer(_("Сперва введи слово на английском"))
    await Start.SetEnglishWord.set()


@dp.message_handler(state=Start.SetEnglishWord)
async def set_english_word(message: Message, state: FSMContext):
    await state.update_data(english_word=message.text)
    await message.answer(_("Теперь введи перевод своего слова"))
    await Start.SetRussianWord.set()


@dp.message_handler(state=Start.SetRussianWord)
async def set_russian_word(message: Message, state: FSMContext):
    await state.update_data(russian_word=message.text)

    data = await state.get_data()
    dict_name = data.get("dict_name")
    english_word = data.get("english_word")
    russian_word = data.get("russian_word")
    tg_id = message.from_user.id
    user_language = message.from_user.language_code

    ########################################################################
    #                        DATABASE Queries                              #
    await db.add_dictionary(tg_id, dict_name)
    dictionary_id_for_start = await db.select_dictionary_id_for_start(tg_id)
    await db.set_current_dictionary(tg_id, dictionary_id_for_start)
    current_dictionary = await db.select_current_dictionary(tg_id)
    await db.add_translate(english_word, russian_word, current_dictionary)

    translate = await db.select_last_translate(current_dictionary)
    translate_id = translate[0]
    await db.set_learning_translate(current_dictionary, translate_id)

    await db.set_user_parameters(tg_id, False, user_language)
    ########################################################################

    await message.answer(_("Итак, название вашего словаря: \"{dict_name}\"\n"
                         "Перевод:\n{english_word} - {russian_word}").format(
        dict_name=dict_name, english_word=english_word, russian_word=russian_word
    ))

    await asyncio.sleep(1)
    await message.answer(_("Теперь ты можешь сам управлять своим переводчиком!\n"
                         "Напиши /menu чтобы посмотреть список команд."), reply_markup=menu)

    await state.finish()
