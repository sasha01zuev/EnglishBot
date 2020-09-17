from aiogram.dispatcher.filters import Command, Text
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.default import menu
from loader import dp


@dp.message_handler(Command("menu"))
async def show_menu(message: Message):
    await message.answer("Выберите пункт из настроек ниже", reply_markup=menu)


@dp.message_handler(Text(equals=["Добавить слово в словарь", "Поменять словарь",
                                 "Создать словарь", "Удалить словарь", "Настройки"]))
async def get_menu_items(message: Message):
    await message.answer(f"Твой выбор - {message.text}.\nУдаление клавиатуры...", reply_markup=ReplyKeyboardRemove())
