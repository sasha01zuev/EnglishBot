from loader import bot


async def on_startup(dp):
    from utils.notify_admins import on_startup_notify

    await on_startup_notify(dp)


async def on_shutdown(dp):
    await bot.close()


if __name__ == '__main__':
    from aiogram import executor
    from handlers import dp

    executor.start_polling(dp, on_startup=on_startup, on_shutdown=on_shutdown)
