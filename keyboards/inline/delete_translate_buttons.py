from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_data import delete_translate_callback
from loader import _

menu_delete_translate_keyboard = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [
            InlineKeyboardButton(text=_("Последнеий добавленый перевод"),
                                 callback_data=delete_translate_callback.new(
                                     item="last_added_word"))
        ],
        [
            InlineKeyboardButton(text=_("Выбрать из 10 последних переводов"),
                                 callback_data=delete_translate_callback.new(
                                     item="last_10_added_words"))
        ],
        [
            InlineKeyboardButton(text=_("Вписать слово вручную"),
                                 callback_data=delete_translate_callback.new(
                                     item="write_word"))
        ],
        [
            InlineKeyboardButton(text=_("Отменить"),
                                 callback_data=delete_translate_callback.new(
                                     item="cancel"))
        ]
    ]
)

