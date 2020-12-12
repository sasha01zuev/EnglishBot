from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, InlineKeyboardButton

from loader import dp, bot
from utils.misc import rate_limit
from keyboards.inline.bot_settings_buttons import bot_settings
from keyboards.inline.callback_data import settings_callback


@dp.callback_query_handler(settings_callback.filter(settings_item="reverse_translate"))
async def reverse_translate(call: CallbackQuery, callback_data: dict):
    await call.answer("Пока что такое не умею 😔", show_alert=True, cache_time=5)



