from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_data import select_language_callback


language_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="English", callback_data=select_language_callback.new(
                lang='en'
            ))
        ],
        [
            InlineKeyboardButton(text="Русский", callback_data=select_language_callback.new(
                lang='ru'
            ))
        ],
        [
            InlineKeyboardButton(text="Українська", callback_data=select_language_callback.new(
                lang='ua'
            ))
        ]
    ]
)
