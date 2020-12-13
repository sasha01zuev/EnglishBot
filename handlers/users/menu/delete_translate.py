from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from keyboards.inline.delete_translate_buttons import menu_delete_translate_keyboard
from loader import dp


@dp.message_handler(Text("🗑Удалить перевод"))
async def delete_translate(message: Message):
    """Show how to delete translate"""
    await message.answer("Как удаляем? 🙃", reply_markup=menu_delete_translate_keyboard)

