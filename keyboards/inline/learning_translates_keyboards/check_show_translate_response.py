from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_data import learning_response_callback


check_show_translate_keyboard = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [
            InlineKeyboardButton(text="Знал",
                                 callback_data=learning_response_callback.new(
                                     is_selected="know"))
        ],
        [
            InlineKeyboardButton(text="Не знал",
                                 callback_data=learning_response_callback.new(
                                     is_selected="showed_unknow"))
        ]
    ]
)

