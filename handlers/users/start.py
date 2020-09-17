import asyncio

from aiogram.dispatcher.filters import CommandStart
from aiogram.types import Message

from loader import dp


@dp.message_handler(CommandStart())
async def show_menu(message: Message):
    await message.answer("Привет! Я вижу ты здесь впервые!\n"
                         "Tы можешь прочитать в описании зачем я exist\n"
                         "Кстати exist - существовать\n")
    await asyncio.sleep(6)
    await message.answer("Ладно, перейдем к делу ...")
    await asyncio.sleep(3)
    await message.answer("Для начала тебе нужно добавить свой первый словарь\n"
                         "Давай я тебе помогу!")
    await asyncio.sleep(4.5)
    await message.answer("Напиши название своего словаря.\n"
                         "По умолчанию - Dictionary 1")
