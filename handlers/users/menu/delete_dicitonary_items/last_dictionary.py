from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.default import menu
from keyboards.inline.callback_data import delete_dictionary_callback, confirm_callback
from keyboards.inline.confirm_buttons import confirm_keyboard

from loader import dp, db, _
from states import DeleteLastDictionary


@dp.callback_query_handler(delete_dictionary_callback.filter(item="last_added_dictionary"))
async def show_last_dictionary(call: CallbackQuery):
    await call.answer(cache_time=5)
    tg_id = call.from_user.id
    await call.message.delete()
    try:
        ######################################################################
        #                            DATABASE Queries                        #
        last_dictionary = await db.select_last_dictionary(tg_id)
        ######################################################################

        await call.message.answer(_('Вы действительно хотите удалить словарь '
                                    '"{dict}?"\n'
                                    'Все слова записанные в этот словарь также удалаяются!').format(
            dict=last_dictionary[2]
        ),
            reply_markup=confirm_keyboard)

        await DeleteLastDictionary.SetDeleteDictionary.set()

    except TypeError:

        select_dictionaries = await db.select_dictionaries(tg_id)
        if not len(select_dictionaries) > 0:
            await call.message.answer(_("У вас нету словарей! Добавьте хоть один словарь."),
                                      reply_markup=menu)
        else:
            await call.message.answer(_("Упс, какая-то ошибка!"), reply_markup=menu)


@dp.callback_query_handler(confirm_callback.filter(item='accept'), state=DeleteLastDictionary.SetDeleteDictionary)
async def accept_deletion(call: CallbackQuery, state: FSMContext):
    await call.answer(_("Удалено"), cache_time=5)
    await call.message.delete()
    tg_id = call.from_user.id
    ######################################################################
    #                            DATABASE Queries                        #
    last_dictionary = await db.select_last_dictionary(tg_id)
    await db.delete_dictionary(last_dictionary[0])
    ######################################################################

    await state.finish()


@dp.callback_query_handler(confirm_callback.filter(item="cancel"), state=DeleteLastDictionary.SetDeleteDictionary)
async def cancel_deletion(call: CallbackQuery, state: FSMContext):
    await call.answer(_("Отмена"), cache_time=5)
    await call.message.delete()
    await state.finish()
