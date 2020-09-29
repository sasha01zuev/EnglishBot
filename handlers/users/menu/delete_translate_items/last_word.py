from aiogram.types import CallbackQuery

from keyboards.inline.delete_translate_buttons import delete_translate_callback, delete_translate_keyboard
from loader import dp


@dp.callback_query_handler(delete_translate_callback.filter(item="last_added_word"))
async def delete_last_word(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=5)
    deletion_type = callback_data['item']
    await call.message.answer(f"Удаление равно {deletion_type}", reply_markup=delete_translate_keyboard)
    # await call.message.edit_reply_markup()
