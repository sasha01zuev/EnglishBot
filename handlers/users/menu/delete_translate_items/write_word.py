from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, Message

from keyboards.inline.confirm_buttons import confirm_keyboard, confirm_callback
from keyboards.inline.delete_translate_buttons import delete_translate_callback
from loader import dp, db
from states import DeleteInputtedTranslate


@dp.callback_query_handler(delete_translate_callback.filter(item="write_word"))
async def write_word(call: CallbackQuery):
    """Set user written word from translate"""
    await call.message.delete()
    await call.answer(cache_time=5)
    await call.message.answer("Введи слово из перевода")
    await DeleteInputtedTranslate.InputWord.set()


@dp.message_handler(state=DeleteInputtedTranslate.InputWord)
async def confirm_deletion(message: Message, state: FSMContext):
    """Find written word in translates of database. Confirmation of deletion written word from translates"""
    await state.update_data(word_name=message.text)
    user_id = message.from_user.id

    ########################################################################
    #                        DATABASE Queries                              #
    current_dictionary = await db.select_current_dictionary(user_id)
    selected_translate = await db.select_translate(current_dictionary, message.text)
    ########################################################################

    try:
        english_word = selected_translate[0][1]
        russian_word = selected_translate[0][2]
        await message.answer(f'Вы действительно хотите удалить '
                             f'"<b>{english_word}</b> - <b>{russian_word}</b>"?',
                             reply_markup=confirm_keyboard)    # Confirmation of deletion
    except IndexError:
        """It raise if not found written translate in current dictionary"""
        await message.answer("В этом словаре перевод <i>не найден</i>!")
        await state.finish()

    except Exception as exc:
        """It raise if unknown error"""
        await message.answer(f"Неизвестная ошибка:\n{exc}")
        await state.finish()


@dp.callback_query_handler(confirm_callback.filter(item="accept"), state=DeleteInputtedTranslate.InputWord)
async def accept_deletion(call: CallbackQuery, state: FSMContext):
    """Deletion written translate from database"""
    await call.answer("Удалено!", cache_time=5)
    await call.message.delete()

    data = await state.get_data()
    word_name = data.get("word_name")    # Fetch word from state
    user_id = call.from_user.id

    try:
        ########################################################################
        #                        DATABASE Queries                              #
        current_dictionary = await db.select_current_dictionary(user_id)
        await db.delete_translate(current_dictionary, word=word_name)    # Accurate deletion written translate from DB
        #                                                                      #
        ########################################################################
    except Exception as exc:
        await call.answer(f"Произошла ошибка!\n{exc}", show_alert=True)

    await state.finish()


@dp.callback_query_handler(confirm_callback.filter(item="cancel"), state=DeleteInputtedTranslate.InputWord)
async def cancel_deletion(call: CallbackQuery, state: FSMContext):
    """Cancel of deletion"""
    await call.answer("Отмена", cache_time=5)
    await state.finish()
    await call.message.delete()
