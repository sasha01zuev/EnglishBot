from aiogram.types import CallbackQuery

from keyboards.inline.callback_data import settings_callback
from loader import dp


@dp.callback_query_handler(settings_callback.filter(settings_item="reverse_translate"))
async def reverse_translate(call: CallbackQuery):
    """Functional not done yet!"""
    await call.answer("Пока что такое не умею 😔", show_alert=True, cache_time=5)
    await call.message.delete()



