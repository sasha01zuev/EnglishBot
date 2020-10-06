from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.buttons.cancel_button import cancel_button
from keyboards.inline.callback_data import delete_dictionary_callback, confirm_callback, select_dictionary_callback, \
    cancel_button_callback
from keyboards.inline.confirm_buttons import confirm_keyboard
from states.delete_dictionary import DeleteDictionary
from loader import dp, db


@dp.callback_query_handler(delete_dictionary_callback.filter(item="list"))
async def show_list_of_dictionaries(call: CallbackQuery):
    await call.answer(cache_time=5)
    tg_id = call.from_user.id
    select_dictionaries = await db.select_dictionaries(tg_id)

    show_dictionaries_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=item[2],
                callback_data=select_dictionary_callback.new(
                    dictionary_id=item[0],
                    dictionary_name=item[2]))] for item in select_dictionaries]
    )
    show_dictionaries_keyboard.add(cancel_button)
    await call.message.answer(f"Выбери словарь из списка:", reply_markup=show_dictionaries_keyboard)

    await call.message.delete()
    await DeleteDictionary.SetDeleteDictionary.set()


@dp.callback_query_handler(cancel_button_callback.filter(state='True'),
                           state=DeleteDictionary.SetDeleteDictionary)
async def cancel_choose_button(call: CallbackQuery, state: FSMContext):
    await call.answer("Отменено", cache_time=5)
    await call.message.delete()
    await state.finish()


@dp.callback_query_handler(select_dictionary_callback.filter(), state=DeleteDictionary.SetDeleteDictionary)
async def deleting_dictionary(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer("Удалено", cache_time=5)
    await call.message.delete()
    dictionary_id = int(callback_data['dictionary_id'])

    #####################################################################################
    #                                 DATABASE Queries                                  #
    await db.delete_dictionary(dictionary_id)
    #####################################################################################
    await state.finish()
