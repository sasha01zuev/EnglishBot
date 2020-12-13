from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.buttons.cancel_button import cancel_button
from keyboards.inline.callback_data import delete_dictionary_callback, confirm_callback, select_dictionary_callback, \
    cancel_button_callback
from keyboards.inline.confirm_buttons import confirm_keyboard
from states import DeleteListDictionary
from loader import dp, db


@dp.callback_query_handler(delete_dictionary_callback.filter(item="list"))
async def show_list_of_dictionaries(call: CallbackQuery):
    """Show list of user dictionaries from DB"""
    await call.answer(cache_time=5)
    user_id = call.from_user.id

    ######################################################################
    #                            DATABASE Queries                        #
    select_dictionaries = await db.select_dictionaries(user_id)  # fetch all user dictionaries
    current_dictionary = await db.select_current_dictionary(user_id)  # fetch current user dictionary
    ######################################################################

    show_dictionaries_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text="{dict} - текущий словарь 📌".format(
                    dict=item[2]
                ),
                callback_data=select_dictionary_callback.new(
                    dictionary_id=item[0],
                    dictionary_name=item[2]))]
            if str(item[0]) == str(current_dictionary)  # Label 📌 near current dictionary
            else [InlineKeyboardButton(  # Else just show dictionary name
                text=item[2],
                callback_data=select_dictionary_callback.new(
                    dictionary_id=item[0],
                    dictionary_name=item[2]))] for item in select_dictionaries]
    )  # Generator for generation list of inline buttons with names with all user dictionaries
    show_dictionaries_keyboard.add(cancel_button)  # Binding inline buttons list of dictionaries with cancel button
    await call.message.answer("Выбери словарь из списка:", reply_markup=show_dictionaries_keyboard)

    await call.message.delete()
    await DeleteListDictionary.SetDeleteDictionary.set()


@dp.callback_query_handler(select_dictionary_callback.filter(),
                           state=DeleteListDictionary.SetDeleteDictionary)
async def confirm_deleting_dictionary(call: CallbackQuery, callback_data: dict, state: FSMContext):
    """Confirm deleting selected dictionary"""
    await call.answer(cache_time=5)
    await call.message.delete()
    dictionary_id = int(callback_data['dictionary_id'])

    try:
        ###############################################################
        #                     DATABASE Queries                        #
        dictionary = await db.select_dictionary(dictionary_id)    # Fetch row of dictionary
        ###############################################################

        await call.message.answer(f'Вы действительно хотите удалить словарь "<b>{dictionary[2]}</b>?"\n'
                                  'Все слова записанные в этот словарь также <i>удалаяются</i>!',
                                  reply_markup=confirm_keyboard)    # dictionary[2] - name of dictionary
        await state.update_data(dictionary_id=dictionary[0])
    except Exception as error:
        await call.message.answer(f"Упс, неизвестная ошибка!\n{error}")
        await state.finish()


@dp.callback_query_handler(confirm_callback.filter(item='accept'),
                           state=DeleteListDictionary.SetDeleteDictionary)
async def deleting_dictionary(call: CallbackQuery, state: FSMContext):
    """Deleting dictionary from database"""
    await call.answer("Удалено", cache_time=5)
    await call.message.delete()

    data = await state.get_data()
    dictionary_id = int(data.get("dictionary_id"))

    #####################################################################################
    #                                 DATABASE Queries                                  #
    await db.delete_dictionary(dictionary_id)    # Deleting select dictionary from database
    #####################################################################################

    await state.finish()


@dp.callback_query_handler(cancel_button_callback.filter(state='True'),
                           state=DeleteListDictionary.SetDeleteDictionary)
async def cancel_choose_button(call: CallbackQuery, state: FSMContext):
    """Cancel choosing a dictionary for deleting"""
    await call.answer("Отмена", cache_time=5)
    await call.message.delete()
    await state.finish()


@dp.callback_query_handler(confirm_callback.filter(item="cancel"),
                           state=DeleteListDictionary.SetDeleteDictionary)
async def cancel_deletion(call: CallbackQuery, state: FSMContext):
    """Cancel deleting a dictionary"""
    await call.answer("Отмена", cache_time=5)
    await call.message.delete()
    await state.finish()
