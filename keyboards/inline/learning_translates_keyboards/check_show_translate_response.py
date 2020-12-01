from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_data import learning_response_callback
from loader import _

check_show_translate_keyboard = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [
            InlineKeyboardButton(text=_("Знал"),
                                 callback_data=learning_response_callback.new(
                                     is_selected="know"))
        ],
        [
            InlineKeyboardButton(text=_("Не знал"),
                                 callback_data=learning_response_callback.new(
                                     is_selected="showed_unknow"))
        ]
    ]
)

