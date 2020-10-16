from aiogram.dispatcher.filters import Command
from aiogram.types import Message

from keyboards.default import menu
from loader import dp, _


@dp.message_handler(Command("menu"))
async def show_menu(message: Message):
    await message.answer(_("Выберите пункт из настроек ниже"), reply_markup=menu)
