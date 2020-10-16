from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery, InlineKeyboardButton

from loader import dp, bot, _
from utils.misc import rate_limit
from keyboards.inline.bot_settings_buttons import bot_settings
from keyboards.inline.select_language import language_keyboard
from keyboards.inline.callback_data import settings_callback, select_language_callback
from states import SelectLanguage


@dp.callback_query_handler(settings_callback.filter(settings_item="change_language"))
async def change_language(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=5)
    await call.message.delete()
    await SelectLanguage.SetLanguage.set()
    await call.message.answer(_("Выбери язык"), reply_markup=language_keyboard)


@dp.callback_query_handler(select_language_callback.filter(lang='en'), state=SelectLanguage.SetLanguage)
async def set_english_lang(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer("Chosen English language", cache_time=5)
    await call.message.delete()
    await state.finish()
    await call.message.answer(_("Выбери язык"), reply_markup=bot_settings)


@dp.callback_query_handler(select_language_callback.filter(lang='ru'), state=SelectLanguage.SetLanguage)
async def set_english_lang(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer("Выбран Русский язык", cache_time=5)
    await call.message.delete()
    await state.finish()
    await call.message.answer(_("Выбери язык"), reply_markup=bot_settings)


@dp.callback_query_handler(select_language_callback.filter(lang='ua'), state=SelectLanguage.SetLanguage)
async def set_english_lang(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer("Вибрано Українську мову", cache_time=5)
    await call.message.delete()
    await state.finish()
    await call.message.answer(_("Выбери язык"), reply_markup=bot_settings)


