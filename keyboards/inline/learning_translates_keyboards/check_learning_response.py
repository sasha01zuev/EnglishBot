from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_data import learning_response_callback


check_response_keyboard = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Знаю",
                                 callback_data=learning_response_callback.new(
                                     is_selected="know"))
        ],
        [
            InlineKeyboardButton(text="Не знаю",
                                 callback_data=learning_response_callback.new(
                                     is_selected="unknow"))
        ],
        [
            InlineKeyboardButton(text="Показать перевод",
                                 callback_data=learning_response_callback.new(
                                     is_selected="show_translate"))
        ]
    ]
)

