# from typing import Tuple, Any
#
# from aiogram.contrib.middlewares.i18n import I18nMiddleware
# from loader import db
# from aiogram.types import User
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
