import asyncpg
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import Message, CallbackQuery

from keyboards.inline.buttons.cancel_button import cancel_button
from keyboards.inline.callback_data import cancel_button_callback
from keyboards.inline.callback_data import select_dictionary_callback
from states import ChangeDictionary
from loader import dp, db, _
from utils.misc import rate_limit


@rate_limit(limit=5)
@dp.message_handler(Text("Поменять словарь"))
async def change_dictionary(message: Message):
    tg_id = message.from_user.id

    select_dictionaries = await db.select_dictionaries(tg_id)
    current_dictionary = await db.select_current_dictionary(tg_id)

    show_dictionaries_keyboard = InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(
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

    await message.answer(_("Выбери словарь из списка:"), reply_markup=show_dictionaries_keyboard)
    await ChangeDictionary.SetChangeDictionary.set()


@dp.callback_query_handler(cancel_button_callback.filter(state='True'),
                           state=ChangeDictionary.SetChangeDictionary)
async def cancel_choose_button(call: CallbackQuery, state: FSMContext):
    await call.answer(cache_time=5)
    await call.message.delete()
    await state.finish()


@dp.callback_query_handler(select_dictionary_callback.filter(), state=ChangeDictionary.SetChangeDictionary)
async def changing_dictionary(call: CallbackQuery, callback_data: dict, state: FSMContext):
    name_selected_dictionary = callback_data['dictionary_name']
    tg_id = call.from_user.id
    id_selected_dictionary = int(callback_data['dictionary_id'])

    try:
        ########################################################################
        #                        DATABASE Queries                              #
        await db.set_current_dictionary(tg_id, id_selected_dictionary)
        ########################################################################

        await call.answer(_('Выбран словарь "{name_selected_dictionary}"').format(
            name_selected_dictionary=name_selected_dictionary
        ), cache_time=5)
        await call.message.delete()
        await state.finish()
    except asyncpg.exceptions.ForeignKeyViolationError:
        await call.answer(_("Этого словаря уже не существует!"), show_alert=True, cache_time=5)
        await call.message.delete()
        await state.finish()
    except:
        await call.answer(_("Упс, какая-то ошибка!"), show_alert=True, cache_time=5)
        await call.message.delete()
        await state.finish()
