from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.buttons.cancel_button import cancel_button
from keyboards.inline.callback_data import delete_dictionary_callback, confirm_callback, select_dictionary_callback, \
    cancel_button_callback
from keyboards.inline.confirm_buttons import confirm_keyboard
from states import DeleteListDictionary
from loader import dp, db, _


@dp.callback_query_handler(delete_dictionary_callback.filter(item="list"))
async def show_list_of_dictionaries(call: CallbackQuery):
    await call.answer(cache_time=5)
    tg_id = call.from_user.id

    select_dictionaries = await db.select_dictionaries(tg_id)
    current_dictionary = await db.select_current_dictionary(tg_id)

    show_dictionaries_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=_("{dict} - текущий словарь 📌").format(
                    dict=item[2]
                ),
                callback_data=select_dictionary_callback.new(
                    dictionary_id=item[0],
                    dictionary_name=item[2]))]
            if str(item[0]) == str(current_dictionary)
            else [InlineKeyboardButton(
                text=item[2],
                callback_data=select_dictionary_callback.new(
                    dictionary_id=item[0],
                    dictionary_name=item[2]))] for item in select_dictionaries]
    )
    show_dictionaries_keyboard.add(cancel_button)
    await call.message.answer(_("Выбери словарь из списка:"), reply_markup=show_dictionaries_keyboard)

    await call.message.delete()
    await DeleteListDictionary.SetDeleteDictionary.set()


@dp.callback_query_handler(select_dictionary_callback.filter(),
                           state=DeleteListDictionary.SetDeleteDictionary)
async def deleting_dictionary(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer(cache_time=5)
    await call.message.delete()
    dictionary_id = int(callback_data['dictionary_id'])

    try:
        #####################################################################################
        #                                 DATABASE Queries                                  #
        dictionary = await db.select_dictionary(dictionary_id)
        #####################################################################################

        await call.message.answer(_('Вы действительно хотите удалить словарь '
                                    '"<b>{dict}</b>" ?\n'
                                    'Все слова записанные в этот словарь также <i>удалаяются</i>!').format(
            dict=dictionary[2]
        ),
            reply_markup=confirm_keyboard)
        await state.update_data(dictionary_id=dictionary[0])
    except:
        await call.message.answer(_("Упс, какая-то ошибка!"))
        await state.finish()


@dp.callback_query_handler(confirm_callback.filter(item='accept'),
                           state=DeleteListDictionary.SetDeleteDictionary)
async def deleting_dictionary(call: CallbackQuery, state: FSMContext):
    await call.answer(_("Удалено"), cache_time=5)
    await call.message.delete()

    data = await state.get_data()
    dictionary_id = int(data.get("dictionary_id"))

    #####################################################################################
    #                                 DATABASE Queries                                  #
    await db.delete_dictionary(dictionary_id)
    #####################################################################################

    await state.finish()


@dp.callback_query_handler(cancel_button_callback.filter(state='True'),
                           state=DeleteListDictionary.SetDeleteDictionary)
async def cancel_choose_button(call: CallbackQuery, state: FSMContext):
    await call.answer(_("Отмена"), cache_time=5)
    await call.message.delete()
    await state.finish()


@dp.callback_query_handler(confirm_callback.filter(item="cancel"),
                           state=DeleteListDictionary.SetDeleteDictionary)
async def cancel_deletion(call: CallbackQuery, state: FSMContext):
    await call.answer(_("Отмена"), cache_time=5)
    await call.message.delete()
    await state.finish()
