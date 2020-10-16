from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, InlineKeyboardButton

from loader import dp, bot, _
from utils.misc import rate_limit
from keyboards.inline.bot_settings_buttons import bot_settings
from keyboards.inline.callback_data import settings_callback


@dp.callback_query_handler(settings_callback.filter(settings_item="reverse_translate"))
async def reverse_translate(call: CallbackQuery, callback_data: dict):
    await call.answer("Вы обратили перевод", cache_time=5)
    # bot_settings.insert(InlineKeyboardButton(text="Обратить",
    #                                          callback_data=settings_callback.new(
    #                                              settings_item="reverse",
    #                                              setting_choose="Lol")))
    setting_choose = callback_data['setting_choose']
    await call.message.answer(f"настрокйка равна {setting_choose}", reply_markup=bot_settings)
    # await call.message.edit_reply_markup()
