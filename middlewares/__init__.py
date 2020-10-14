from aiogram import Dispatcher

from .throttling import ThrottlingMiddleware
from .database import SetDBMessage
# from .language_middleware import ACLMiddleware
# from data.config import I18N_DOMAIN, LOCALES_DIR


def setup(dp: Dispatcher):
    dp.middleware.setup(ThrottlingMiddleware())
    dp.middleware.setup(SetDBMessage())
    # i18n = ACLMiddleware(I18N_DOMAIN, LOCALES_DIR)
    # dp.middleware.setup(i18n)
    # return i18n

