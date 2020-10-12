from aiogram import types
from loader import dp


@dp.message_handler()
async def echo_n_send_to_admin(message: types.Message):
    await message.answer(message.text)

