from aiogram.types import CallbackQuery

from keyboards.inline.callback_data import delete_dictionary_callback
from loader import dp


@dp.callback_query_handler(delete_dictionary_callback.filter(item="cancel"))
async def cancel(call: CallbackQuery):
    """Cancel choosing a dictionary for deleting"""
    await call.answer(cache_time=5)
    await call.message.delete()
