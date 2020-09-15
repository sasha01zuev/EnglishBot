from app import bot, dp

from aiogram.types import Message

@dp.message_handler()
async def echo(message: Message):
    await message.answer(text=message.text)