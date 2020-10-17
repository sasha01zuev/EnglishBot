from aiogram import types
from loader import dp, _


@dp.message_handler()
async def echo(message: types.Message):
    await message.answer(_("Не понял команды! 🤨😲"))

