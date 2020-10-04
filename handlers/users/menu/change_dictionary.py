from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from loader import dp, db
from utils.misc import rate_limit
from keyboards.inline.callback_data import select_dictionary_callback
from keyboards.inline.buttons.cancel_button import cancel_button
from keyboards.inline.callback_data import cancel_button_callback


@rate_limit(limit=5)
@dp.message_handler(Text("Поменять словарь"))
async def change_dictionary(message: Message):
    tg_id = message.from_user.id
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

    await message.answer(f"Выбиери словарь из списка:", reply_markup=show_dictionaries_keyboard)


@dp.callback_query_handler(cancel_button_callback.filter(state='True'))
async def cancel_choose_button(call: CallbackQuery):
    await call.answer(cache_time=5)
    await call.message.delete()


@dp.callback_query_handler(select_dictionary_callback.filter())
async def write_word(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=5)
    name_selected_dictionary = callback_data['dictionary_name']
    tg_id = call.from_user.id
    id_selected_dictionary = int(callback_data['dictionary_id'])
    await call.message.delete()

    ########################################################################
    #                        DATABASE Queries                              #
    await db.set_current_dictionary(tg_id, id_selected_dictionary)
    ########################################################################
    await call.message.answer(f"Выбран словарь '{name_selected_dictionary}'")
