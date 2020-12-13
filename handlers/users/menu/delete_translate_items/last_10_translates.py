from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.buttons.cancel_button import cancel_button
from keyboards.inline.callback_data import cancel_button_callback
from keyboards.inline.callback_data import select_translate_callback, confirm_callback
from keyboards.inline.confirm_buttons import confirm_keyboard
from keyboards.inline.delete_translate_buttons import delete_translate_callback
from loader import dp, db
from states import DeleteTranslate


@dp.callback_query_handler(delete_translate_callback.filter(item="last_10_added_words"))
async def delete_last_10_translates(call: CallbackQuery):
    """Show 10 last translates in inline buttons from current dictionary"""
    await call.message.delete()
    await call.answer(cache_time=5)
    user_id = call.from_user.id

    ############################################################################
    #                            DATABASE Queries                              #
    current_dictionary = await db.select_current_dictionary(user_id)    # Fetch current user dictionary
    last_10_translates = await db.select_last_10_translates(current_dictionary)  # Fetch last 10 translates current dict
    ############################################################################

    show_last_10th_translates_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(
                text=f'{item[1]} - {item[2]}',
                callback_data=select_translate_callback.new(
                    dictionary_id=item[3],
                    english_word=item[1],
                    russian_word=item[2]
                )
            )
            ] for item in last_10_translates
        ]
    )    # Generator for generation list of names inline buttons of last 10 translates
    show_last_10th_translates_keyboard.row(cancel_button)    # Binding buttons list of translates with cancel button

    await call.message.answer('Последние 10 переводов:', reply_markup=show_last_10th_translates_keyboard)
    await DeleteTranslate.SetDeleteTranslate.set()


@dp.callback_query_handler(cancel_button_callback.filter(state='True'), state=DeleteTranslate.SetDeleteTranslate)
async def cancel_choose_button(call: CallbackQuery, state: FSMContext):
    """Cancel choosing translate"""
    await call.answer("Отмена", cache_time=5)
    await call.message.delete()
    await state.finish()


@dp.callback_query_handler(select_translate_callback.filter(), state=DeleteTranslate.SetDeleteTranslate)
async def confirm_deletion(call: CallbackQuery, callback_data: dict, state: FSMContext):
    """Confirm deletion selected translate"""
    await call.message.delete()
    await call.answer(cache_time=5)

    id_selected_dictionary = int(callback_data['dictionary_id'])
    english_word = callback_data['english_word']
    russian_word = callback_data['russian_word']

    await state.update_data(english_word=english_word)
    await state.update_data(russian_word=russian_word)
    await state.update_data(current_dictionary_id=id_selected_dictionary)

    await call.message.answer(f"Вы действительно хотите удалить это перевод?\n"
                              f"<b>{english_word}</b> - <b>{russian_word}</b>",
                              reply_markup=confirm_keyboard)


@dp.callback_query_handler(confirm_callback.filter(item="accept"), state=DeleteTranslate.SetDeleteTranslate)
async def accept_deletion(call: CallbackQuery, state: FSMContext):
    """Deletion selected translate from database"""
    await call.answer("Удалено!", cache_time=5)
    await call.message.delete()

    await state.update_data()
    data = await state.get_data()
    current_dictionary_id = data.get("current_dictionary_id")
    english_word = data.get("english_word")
    russian_word = data.get("russian_word")

    #####################################################################################
    #                                 DATABASE Queries                                  #
    await db.delete_translate_accurate(current_dictionary_id, english_word, russian_word)   # Deletion translate
    #                                                                                   #
    #####################################################################################

    await state.finish()


@dp.callback_query_handler(confirm_callback.filter(item="cancel"), state=DeleteTranslate.SetDeleteTranslate)
async def cancel_deletion(call: CallbackQuery, state: FSMContext):
    """Cancel deletion of translate"""
    await call.answer("Отмена", cache_time=5)
    await call.message.delete()
    await state.finish()
