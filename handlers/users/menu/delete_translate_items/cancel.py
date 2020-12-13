from aiogram.types import CallbackQuery

from keyboards.inline.delete_translate_buttons import delete_translate_callback
from loader import dp


@dp.callback_query_handler(delete_translate_callback.filter(item="cancel"))
async def cancel(call: CallbackQuery):
    """Cancel choosing deleting a translate"""
    await call.answer(cache_time=5)
    await call.message.delete()
