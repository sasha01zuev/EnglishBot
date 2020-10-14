# from typing import Tuple, Any
#
# from aiogram.contrib.middlewares.i18n import I18nMiddleware
# from loader import db
# from aiogram.types import User
# from data.config import I18N_DOMAIN, LOCALES_DIR
#
#
# async def get_language():
#     current_user = User.get_current()
#     user_lang = await db.get_user_language(current_user.id)
#     return user_lang
#
#
# class ACLMiddleware(I18nMiddleware):
#     async def get_user_locale(self, action: str, args: Tuple[Any]) -> str:
#         current_user = User.get_current()
#         user_lang = await db.get_user_language(current_user.id)
#         return user_lang or current_user.locale
#
#
# def setup_middleware(dp):
#     # Устанавливаем миддлварь
#     i18n = ACLMiddleware(I18N_DOMAIN, LOCALES_DIR)
#     dp.middleware.setup(i18n)
#     return i18n


