import asyncpg
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import Message, CallbackQuery

from keyboards.inline.buttons.cancel_button import cancel_button
from keyboards.inline.callback_data import cancel_button_callback
from keyboards.inline.callback_data import select_dictionary_callback
from loader import dp, db
from states import ChangeDictionary
from utils.misc import rate_limit


@rate_limit(limit=5)  # Antispam
@dp.message_handler(Text("Поменять словарь"))
async def showing_dictionaries(message: Message):
    """Showing all user dictionaries for select current"""
    user_id = message.from_user.id

    ########################################################################
    #                        DATABASE Queries                              #
    select_dictionaries = await db.select_dictionaries(user_id)
    current_dictionary = await db.select_current_dictionary(user_id)
    ########################################################################

    show_dictionaries_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(
            text=f"{item[2]} - текущий словарь 📌",
            callback_data=select_dictionary_callback.new(
                dictionary_id=item[0],
                dictionary_name=item[2]))]
                         if str(item[0]) == str(current_dictionary)  # Label 📌 near current dictionary name
                         else [InlineKeyboardButton(text=item[2],  # Just show dictionary name
                                                    callback_data=select_dictionary_callback.new(
                                                        dictionary_id=item[0],
                                                        dictionary_name=item[2]))] for item in select_dictionaries]
    )  # Generation list of inline buttons with dictionaries names
    show_dictionaries_keyboard.add(cancel_button)  # Binding inline buttons list of dictionaries with cancel button

    await message.answer("Выбери словарь из списка:", reply_markup=show_dictionaries_keyboard)  # Showing all user
    # dictionaries for select
    await ChangeDictionary.SetChangeDictionary.set()


@dp.callback_query_handler(cancel_button_callback.filter(state='True'),
                           state=ChangeDictionary.SetChangeDictionary)
async def cancel_choose_button(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=5)
    await call.message.delete()
    await state.finish()


@dp.callback_query_handler(select_dictionary_callback.filter(), state=ChangeDictionary.SetChangeDictionary)
async def changing_dictionary(call: CallbackQuery, callback_data: dict, state: FSMContext):
    """Changing current dictionary in database"""
    name_selected_dictionary = callback_data['dictionary_name']
    user_id = call.from_user.id
    id_selected_dictionary = int(callback_data['dictionary_id'])

    try:
        ########################################################################
        #                        DATABASE Queries                              #
        await db.set_current_dictionary(user_id, id_selected_dictionary)
        ########################################################################

        await call.answer('Выбран словарь "{name_selected_dictionary}"', cache_time=5)
        await call.message.delete()
        await state.finish()
    except asyncpg.exceptions.ForeignKeyViolationError:
        """It raised if selected dictionary doesn't exist"""
        await call.answer("Этого словаря уже не существует!", show_alert=True, cache_time=5)
        await call.message.delete()
        await state.finish()
    except:
        """It raised when unknown error"""
        await call.answer("Упс, какая-то ошибка!", show_alert=True, cache_time=5)
        await call.message.delete()
        await state.finish()
