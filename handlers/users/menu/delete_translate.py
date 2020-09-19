from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ReplyKeyboardRemove

from loader import dp
from utils.misc import rate_limit


@rate_limit(limit=5)
@dp.message_handler(Text("Удалить перевод"))
async def delete_translate(message: Message):
    await message.answer(f"Твой выбор - {message.text}.", reply_markup=ReplyKeyboardRemove())
