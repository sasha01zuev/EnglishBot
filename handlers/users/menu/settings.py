from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from loader import dp, bot, _
from utils.misc import rate_limit
from keyboards.inline.bot_settings_buttons import bot_settings


@dp.message_handler(Text("Настройки"))
async def settings(message: Message):
    await message.answer(_("Настройки бота:"), reply_markup=bot_settings)


