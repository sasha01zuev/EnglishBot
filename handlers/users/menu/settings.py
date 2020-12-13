from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from loader import dp, bot
from utils.misc import rate_limit
from keyboards.inline.bot_settings_buttons import bot_settings


@dp.message_handler(Text("⚙Настройки"))
async def settings(message: Message):
    """Show settings for user"""
    await message.answer("Настройки бота:", reply_markup=bot_settings)


