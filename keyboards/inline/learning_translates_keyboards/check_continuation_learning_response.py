from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_data import start_learning_callback
from loader import _

check_continuation_learning_keyboard = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [
            InlineKeyboardButton(text=_("Учить дальше"),
                                 callback_data=start_learning_callback.new(
                                     is_selected="True"))
        ],
        [
            InlineKeyboardButton(text=_("Стоп"),
                                 callback_data=start_learning_callback.new(
                                     is_selected="False"))
        ]
    ]
)