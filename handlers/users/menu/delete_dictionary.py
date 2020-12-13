from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from keyboards.inline.menu_delete_dictionary import delete_translate_keyboard
from loader import dp
from utils.misc import rate_limit


@rate_limit(limit=5)  # Antispam
@dp.message_handler(Text("🗑Удалить словарь"))
async def delete_dictionary(message: Message):
    """Show how to delete dictionary"""
    await message.answer("Как удаляем? 🙃", reply_markup=delete_translate_keyboard)
