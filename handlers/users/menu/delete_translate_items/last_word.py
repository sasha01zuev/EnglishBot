from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline.callback_data import confirm_callback, delete_translate_callback
from keyboards.inline.confirm_buttons import confirm_keyboard

from loader import dp, db
from states.delete_last_translate import DeleteLastTranslate


@dp.callback_query_handler(delete_translate_callback.filter(item="last_added_word"))
async def delete_last_word(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=5)
    tg_id = call.from_user.id

    ######################################################################
    #                            DATABASE Queries                        #
    current_dictionary = await db.select_current_dictionary(tg_id)
    last_translate = await db.select_last_translate(current_dictionary)
    ######################################################################

    print(last_translate)
    english_word = last_translate[1]
    russian_word = last_translate[2]
    id_dictionary_selected_translate = last_translate[0]

    print(f"{tg_id} - {english_word} - {russian_word}")
    await call.message.answer(f"Вы действительно хотите удалить это перевод?\n"
                              f"{english_word} - {russian_word}", reply_markup=confirm_keyboard)

    await DeleteLastTranslate.SetDeleteLastTranslate.set()
    await call.message.delete()


@dp.callback_query_handler(confirm_callback.filter(item="accept"), state=DeleteLastTranslate.SetDeleteLastTranslate)
async def accept_deletion(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.message.delete()
    await call.answer(cache_time=5)
    tg_id = call.from_user.id

    #####################################################################################
    #                                 DATABASE Queries                                  #
    current_dictionary = await db.select_current_dictionary(tg_id)
    last_translate = await db.select_last_translate(current_dictionary)
    english_word = last_translate[1]
    russian_word = last_translate[2]
    await db.delete_translate_accurate(current_dictionary, english_word, russian_word)
    #                                                                                   #
    #####################################################################################

    await call.message.answer("Удалено!")
    await state.finish()


@dp.callback_query_handler(confirm_callback.filter(item="cancel"), state=DeleteLastTranslate.SetDeleteLastTranslate)
async def cancel_deletion(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=5)
    await call.message.delete()
    await state.finish()
