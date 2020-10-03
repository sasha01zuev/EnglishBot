from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_data import delete_translate_callback

menu_delete_translate_keyboard = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Последнее добавленое слово",
                                 callback_data=delete_translate_callback.new(
                                     item="last_added_word"))
        ],
        [
            InlineKeyboardButton(text="Выбрать из 10 последних слов",
                                 callback_data=delete_translate_callback.new(
                                     item="last_10_added_words"))
        ],
        [
            InlineKeyboardButton(text="Вписать слово вручную",
                                 callback_data=delete_translate_callback.new(
                                     item="write_word"))
        ],
        [
            InlineKeyboardButton(text="Отменить",
                                 callback_data=delete_translate_callback.new(
                                     item="cancel"))
        ]
    ]
)

