from aiogram import types
from aiogram.types import ContentType, Message

from loader import dp, _


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(_("Не понял команды! 🤨😲"))


@dp.message_handler(content_types=ContentType.PHOTO)
async def photo_echo(message: Message):
    await message.answer(_("Я пока-что не принимаю фото! 🤨😲"))
    print(message.photo[-1].file_id)

