from aiogram.types import CallbackQuery, ReplyKeyboardRemove, Message
from aiogram.dispatcher import FSMContext

from keyboards.inline.delete_translate_buttons import delete_translate_callback, delete_translate_keyboard
from keyboards.inline.confirm_buttons import confirm_keyboard, confirm_callback
from loader import dp, db
from states.delete_inputted_translate import DeleteInputtedTranslate


@dp.callback_query_handler(delete_translate_callback.filter(item="write_word"))
async def write_word(call: CallbackQuery, callback_data: dict):
    await call.message.delete()
    await call.answer(cache_time=5)
    deletion_type = callback_data['item']
    await call.message.answer("Введи своё слово")
    # await call.message.edit_reply_markup()
    await DeleteInputtedTranslate.InputWord.set()


@dp.message_handler(state=DeleteInputtedTranslate.InputWord)
async def check_deletion(message: Message, state: FSMContext):
    await state.update_data(word_name=message.text)
    tg_id = message.from_user.id

    ########################################################################
    #                        DATABASE Queries                              #
    current_dictionary = await db.select_current_dictionary(tg_id)
    selected_translate = await db.select_translate(current_dictionary,
                                                   word=message.text)
    #                                                                      #
    ########################################################################
    try:
        english_word = selected_translate[0][1]
        russian_word = selected_translate[0][2]

        await message.answer(f'Вы действительно хотите удалить "{english_word} - {russian_word}"?',
                             reply_markup=confirm_keyboard)
    except IndexError:
        await message.answer("В этом словаре перевод не найден!")
        await state.finish()


@dp.callback_query_handler(confirm_callback.filter(item="accept"), state=DeleteInputtedTranslate.InputWord)
async def accept_deletion(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.delete()
    await call.answer(cache_time=5)
    data = await state.get_data()
    word_name = data.get("word_name")
    tg_id = call.from_user.id

    ########################################################################
    #                        DATABASE Queries                              #
    current_dictionary = await db.select_current_dictionary(tg_id)
    selected_translate = await db.select_translate(current_dictionary,
                                                   word=word_name)
    await db.delete_translate(current_dictionary, word=word_name)
    #                                                                      #
    ########################################################################

    english_word = selected_translate[0][1]
    russian_word = selected_translate[0][2]

    await call.message.answer(f'Принято. Удаление "{english_word} - {russian_word}"...')
    await state.finish()


@dp.callback_query_handler(confirm_callback.filter(item="cancel"), state=DeleteInputtedTranslate.InputWord)
async def accept_deletion(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=5)
    await state.finish()
    await call.message.delete()
