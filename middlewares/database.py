from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from loader import db


class SetDBMessage(BaseMiddleware):
    """Tracker of user last action"""
    async def on_process_message(self, message: types.Message, data: dict):

        user_id = message.from_user.id
        message_text = message.text

        await db.add_message(user_id, message_text)
        await db.add_last_action(user_id)

    async def on_process_callback_query(self, cq: types.CallbackQuery, data: dict):
        user_id = cq.from_user.id
        message_text = str(data['callback_data'])

        await db.add_message(user_id, message_text)
        await db.add_last_action(user_id)
