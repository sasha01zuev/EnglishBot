from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_data import delete_dictionary_callback

delete_translate_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Последнеий добавленый словарь",
                                 callback_data=delete_dictionary_callback.new(
                                     item="last_added_dictionary"))
        ],
        [
            InlineKeyboardButton(text="Показать список",
                                 callback_data=delete_dictionary_callback.new(
                                     item="list"))
        ],
        [
            InlineKeyboardButton(text="Отменить 🚫",
                                 callback_data=delete_dictionary_callback.new(
                                     item="cancel"))
        ]
    ]
)

