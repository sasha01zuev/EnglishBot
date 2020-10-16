from aiogram.types import CallbackQuery

from keyboards.inline.delete_translate_buttons import delete_translate_callback
from loader import dp, _


@dp.callback_query_handler(delete_translate_callback.filter(item="cancel"))
async def cancel(call: CallbackQuery, callback_data: dict):
    await call.answer(_("Отмена"), cache_time=5)

    await call.message.delete()

    # await call.message.edit_reply_markup()