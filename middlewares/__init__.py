from aiogram import Dispatcher

from .throttling import ThrottlingMiddleware
from .database import SetDBMessage


def setup(dp: Dispatcher):
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(SetDBMessage())
