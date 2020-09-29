from aiogram.types import CallbackQuery

from keyboards.inline.delete_translate_buttons import delete_translate_callback
from loader import dp


@dp.callback_query_handler(delete_translate_callback.filter(item="cancel"))
async def cancel(call: CallbackQuery, callback_data: dict):
    await call.answer("Отмена", cache_time=5)
    deletion_type = callback_data['item']
    await call.message.delete()
    await call.message.answer(f"Удаление равно {deletion_type}")
    # await call.message.edit_reply_markup()