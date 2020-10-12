from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message

from keyboards.default import menu
from loader import dp


@dp.message_handler(Command("menu"))
async def show_menu(message: Message):
    await message.answer("Выберите пункт из настроек ниже", reply_markup=menu)
