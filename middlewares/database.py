from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from loader import db


class SetDBMessage(BaseMiddleware):

    async def on_process_message(self, message: types.Message, data: dict):
        tg_id = message.from_user.id
        message_text = message.text

        try:
            await db.add_message(tg_id, message_text)
            await db.add_last_action(tg_id)
        except:
            pass

    async def on_process_callback_query(self, cq: types.CallbackQuery, data: dict):
        tg_id = cq.from_user.id
        message_text = str(data['callback_data'])


        try:
            await db.add_message(tg_id, message_text)
            await db.last_action(tg_id)
        except:
            pass