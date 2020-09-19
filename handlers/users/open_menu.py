from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.default import menu
from loader import dp
from utils.misc import rate_limit


# @rate_limit(limit=5)
@dp.message_handler(Command("menu"))
async def show_menu(message: Message):
    await message.answer("Выберите пункт из настроек ниже", reply_markup=menu)
