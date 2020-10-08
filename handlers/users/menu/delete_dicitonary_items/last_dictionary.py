import aiogram
from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.default import menu
from keyboards.inline.callback_data import delete_dictionary_callback, confirm_callback
from keyboards.inline.confirm_buttons import confirm_keyboard

from loader import dp, db
from states.delete_dictionary import DeleteDictionary


@dp.callback_query_handler(delete_dictionary_callback.filter(item="last_added_dictionary"))
async def show_last_dictionary(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=5)
    tg_id = call.from_user.id
    await call.message.delete()
    try:
        ######################################################################
        #                            DATABASE Queries                        #
        last_dictionary = await db.select_last_dictionary(tg_id)
        ######################################################################

        await call.message.answer(f'Вы действительно хотите удалить словарь '
                                  f'"{last_dictionary[2]}?"\n'
                                  f'Все слова записанные в этот словарь также удалаяются!',
                                  reply_markup=confirm_keyboard)

        await DeleteDictionary.SetDeleteDictionary.set()

    except TypeError:

        select_dictionaries = await db.select_dictionaries(tg_id)
        if not len(select_dictionaries) > 0:
            await call.message.answer("У вас нету словарей! Добавьте хоть один словарь.",
                                      reply_markup=menu)
        else:
            await call.message.answer("Упс, какая-то ошибка!", reply_markup=menu)


@dp.callback_query_handler(confirm_callback.filter(item='accept'), state=DeleteDictionary.SetDeleteDictionary)
async def accept_deletion(call: CallbackQuery, state: FSMContext):
    await call.answer("Удалено", cache_time=5)
    await call.message.delete()

    tg_id = call.from_user.id
    ######################################################################
    #                            DATABASE Queries                        #
    last_dictionary = await db.select_last_dictionary(tg_id)
    await db.delete_dictionary(last_dictionary[0])
    ######################################################################

    await state.finish()


@dp.callback_query_handler(confirm_callback.filter(item="cancel"), state=DeleteDictionary.SetDeleteDictionary)
async def cancel_deletion(call: CallbackQuery, state: FSMContext):
    await call.answer("Отмена", cache_time=5)
    await call.message.delete()
    await state.finish()
