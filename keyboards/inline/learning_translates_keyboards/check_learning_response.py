from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_data import learning_response_callback
from loader import _

check_response_keyboard = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [
            InlineKeyboardButton(text=_("Знаю"),
                                 callback_data=learning_response_callback.new(
                                     is_selected="know"))
        ],
        [
            InlineKeyboardButton(text=_("Не знаю"),
                                 callback_data=learning_response_callback.new(
                                     is_selected="unknow"))
        ],
        [
            InlineKeyboardButton(text=_("Показать перевод"),
                                 callback_data=learning_response_callback.new(
                                     is_selected="show_translate"))
        ]
    ]
)

