from aiogram.dispatcher.filters import Text
from aiogram.types import Message

from keyboards.inline.menu_delete_dictionary import delete_translate_keyboard
from loader import dp
from utils.misc import rate_limit


@rate_limit(limit=5)
@dp.message_handler(Text("Удалить словарь"))
async def delete_dictionary(message: Message):
    await message.answer("Выберите пункт", reply_markup=delete_translate_keyboard)
