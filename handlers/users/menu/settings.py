from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from loader import dp, bot
from utils.misc import rate_limit
from keyboards.inline.bot_settings_buttons import bot_settings


@dp.message_handler(Text("Настройки"))
async def settings(message: Message):
    await message.answer("Настройки бота:", reply_markup=bot_settings)


# @dp.callback_query_handler(settings_callback.filter(settings_item="reverse_translate"))
# async def reverse_translate(call: CallbackQuery, callback_data: dict):
#     await call.answer("Вы обратили перевод", cache_time=5)
#     setting_choose = callback_data.get("setting_choose")
#     await call.message.answer(f"настрокйка равна {setting_choose}")
#     await call.message.edit_reply_markup()
