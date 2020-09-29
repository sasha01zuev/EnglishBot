from aiogram.types import CallbackQuery

from keyboards.inline.delete_translate_buttons import delete_translate_callback, delete_translate_keyboard
from loader import dp
from keyboards.inline.confirm_buttons import confirm_keyboard


@dp.callback_query_handler(delete_translate_callback.filter(item="last_10_added_words"))
async def delete_last_10_word(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=5)
    deletion_type = callback_data['item']
    await call.message.answer(f'Удаление равно {deletion_type}', reply_markup=confirm_keyboard)
    await call.message.edit_reply_markup()
