from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from loader import dp

from keyboards.inline.delete_translate_buttons import delete_translate_keyboard


@dp.message_handler(Text("Удалить перевод"))
async def delete_translate(message: Message):
    await message.answer("Удаление бота", reply_markup=delete_translate_keyboard)
