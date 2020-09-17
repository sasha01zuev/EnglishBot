import logging

from aiogram import Dispatcher

from data.config import ADMINS_ID


async def on_startup_notify(dp: Dispatcher):
    for admin in ADMINS_ID:
        try:
            await dp.bot.send_message(admin, "***Это сообщение видят только админы***\n"
                                             "            Саша меня только что запустил"
                                             "\nНапиши /menu чтобы увидеть список команд")
        except Exception as err:
            logging.exception(err)


async def on_shutdown_notify(dp: Dispatcher):
    for admin in ADMINS_ID:
        try:
            await dp.bot.send_message(admin, "***Это сообщение видят только админы***\n"
                                             "            Саша меня только что вырубил")
        except Exception as err:
            logging.exception(err)
