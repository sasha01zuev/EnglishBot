from aiogram import types
from data.config import MAIN_ADMIN
from loader import dp, bot



@dp.message_handler()
async def echo_n_send_to_admin(message: types.Message):
    await message.answer(message.text)
    await bot.send_message(MAIN_ADMIN, text=f"{message.from_user.first_name} "
                                            f"{message.from_user.last_name} "
                                            f"{message.from_user.id}:  "
                                            f"{message.text}")
