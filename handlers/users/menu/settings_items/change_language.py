from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, InlineKeyboardButton

from loader import dp, bot
from utils.misc import rate_limit
from keyboards.inline.bot_settings_buttons import bot_settings
from keyboards.inline.callback_data import settings_callback


@dp.callback_query_handler(settings_callback.filter(settings_item="change_language"))
async def change_language(call: CallbackQuery, callback_data: dict):
    await call.answer("Вы изменили язык", cache_time=5)
    setting_choose = callback_data.get("setting_choose")
    #
    # await call.message.delete()
    # await call.message.answer(f"настрокйка равна {setting_choose}", reply_markup=bot_settings)

