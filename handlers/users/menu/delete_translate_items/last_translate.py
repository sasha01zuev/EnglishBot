from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.default import menu
from keyboards.inline.callback_data import confirm_callback, delete_translate_callback, select_dictionary_callback
from keyboards.inline.confirm_buttons import confirm_keyboard
from loader import dp, db
from states import DeleteLastTranslate


@dp.callback_query_handler(delete_translate_callback.filter(item="last_added_word"))
async def delete_last_word(call: CallbackQuery):
    """Confirmation of deletion last translate"""
    await call.answer(cache_time=5)
    user_id = call.from_user.id
    try:
        """It works right when there are more than 0 translates in current dictionary"""
        ######################################################################
        #                            DATABASE Queries                        #
        current_dictionary = await db.select_current_dictionary(user_id)
        last_translate = await db.select_last_translate(current_dictionary)  # Last translate from current dictionary
        ######################################################################

        print(last_translate)
        if last_translate:
            english_word = last_translate[1]
            russian_word = last_translate[2]

            await call.message.answer(f"Вы действительно хотите удалить это перевод?\n"
                                      f"<b>{english_word}</b> - <b>{russian_word}</b>",
                                      reply_markup=confirm_keyboard)  # Query confirmation of deletion of translate

            await DeleteLastTranslate.SetDeleteLastTranslate.set()
            await call.message.delete()
        else:
            await call.message.delete()
            await call.message.answer('Нету переводов!')
    except TypeError:
        select_dictionaries = await db.select_dictionaries(user_id)    # All user dictionaries
        if len(select_dictionaries) > 0:
            """It raised when current dictionary was deleted. It offer to select new current dictionary"""
            show_dictionaries_keyboard = InlineKeyboardMarkup(
                inline_keyboard=[
                    [InlineKeyboardButton(
                        text=item[2],
                        callback_data=select_dictionary_callback.new(
                            dictionary_id=item[3],
                            dictionary_name=item[2]))] for item in select_dictionaries]
            )    # Generate inline buttons with user dictionaries
            await call.message.answer("Так как вы удалили свой текущий словарь, \n"
                                      "то вам придется выбрать <i>новый текущий словарь</i>",
                                      reply_markup=show_dictionaries_keyboard)    # Selecting current dict
            await DeleteLastTranslate.SetDeleteLastTranslate.set()
            await call.message.delete()
        else:
            """It raised when quantity of dictionaries equals 0"""
            await call.message.delete()
            await call.message.answer("У вас нету словарей! Добавьте хоть один словарь.", reply_markup=menu)



@dp.callback_query_handler(confirm_callback.filter(item="accept"), state=DeleteLastTranslate.SetDeleteLastTranslate)
async def accept_deletion(call: CallbackQuery, state: FSMContext):
    """Deletion last translate from database"""
    await call.answer("Удалено!", cache_time=5)
    await call.message.delete()

    user_id = call.from_user.id

    ###############################################################################
    #                                 DATABASE Queries                            #
    current_dictionary = await db.select_current_dictionary(user_id)
    last_translate = await db.select_last_translate(current_dictionary)
    english_word = last_translate[1]
    russian_word = last_translate[2]
    await db.delete_translate_accurate(current_dictionary, english_word, russian_word)  # Accurate deletion of translate
    ################################################################################

    await state.finish()


@dp.callback_query_handler(confirm_callback.filter(item="cancel"),
                           state=DeleteLastTranslate.SetDeleteLastTranslate)
async def cancel_deletion(call: CallbackQuery, state: FSMContext):
    """Cancel of deletion last translate"""
    await call.answer("Отмена", cache_time=5)
    await call.message.delete()
    await state.finish()


@dp.callback_query_handler(select_dictionary_callback.filter(), state=DeleteLastTranslate.SetDeleteLastTranslate)
async def changing_dictionary(call: CallbackQuery, callback_data: dict, state: FSMContext):
    """Changing current dictionary if raised exception at deletion translate"""
    name_selected_dictionary = callback_data['dictionary_name']
    id_selected_dictionary = int(callback_data['dictionary_id'])
    user_id = call.from_user.id

    ########################################################################
    #                        DATABASE Queries                              #
    await db.set_current_dictionary(user_id, id_selected_dictionary)
    ########################################################################

    await call.answer(f"Выбран словарь '{name_selected_dictionary}'", cache_time=5)
    await call.message.delete()
    await call.message.answer("Теперь, чтобы удалить перевод, вы должны его c начала <i>добавить</i>!",
                              reply_markup=menu)

    await state.finish()
