from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.default import menu
from keyboards.inline.callback_data import delete_dictionary_callback, confirm_callback
from keyboards.inline.confirm_buttons import confirm_keyboard
from loader import dp, db
from states import DeleteLastDictionary


@dp.callback_query_handler(delete_dictionary_callback.filter(item="last_added_dictionary"))
async def show_last_dictionary(call: CallbackQuery):
    """Show last added dictionary in Inline Button"""
    await call.answer(cache_time=5)
    await call.message.delete()
    user_id = call.from_user.id

    try:
        """It works right when there are more than 0 dictionaries"""
        ######################################################################
        #                            DATABASE Queries                        #
        last_dictionary = await db.select_last_dictionary(user_id)    # Fetch last user dictionary
        ######################################################################

        await call.message.answer(f'Вы действительно хотите удалить словарь "<b>{last_dictionary[2]}</b>?"\n'
                                  'Все слова записанные в этот словарь также <i>удалаяются</i>!',
                                  reply_markup=confirm_keyboard)    # last_dictionary[2] - name of dictionary
        await DeleteLastDictionary.SetDeleteDictionary.set()

    except TypeError:
        """It raised when quantity of dictionaries equals 0"""
        select_dictionaries = await db.select_dictionaries(user_id)
        if not len(select_dictionaries) > 0:
            await call.message.answer("У вас нету словарей! Добавьте хоть один словарь.",
                                      reply_markup=menu)
        else:   # Just in case
            await call.message.answer("Упс, какая-то ошибка!", reply_markup=menu)


@dp.callback_query_handler(confirm_callback.filter(item='accept'), state=DeleteLastDictionary.SetDeleteDictionary)
async def accept_deletion(call: CallbackQuery, state: FSMContext):
    """Deleting dictionary from database"""
    await call.answer("Удалено", cache_time=5)
    await call.message.delete()
    user_id = call.from_user.id

    ######################################################################
    #                            DATABASE Queries                        #
    last_dictionary = await db.select_last_dictionary(user_id)    # Fetch last user dictionary
    await db.delete_dictionary(last_dictionary[0])    # Deleting selected dictionary
    ######################################################################

    await state.finish()


@dp.callback_query_handler(confirm_callback.filter(item="cancel"), state=DeleteLastDictionary.SetDeleteDictionary)
async def cancel_deletion(call: CallbackQuery, state: FSMContext):
    """Cancel deleting a dictionary"""
    await call.answer("Отмена", cache_time=5)
    await call.message.delete()
    await state.finish()
