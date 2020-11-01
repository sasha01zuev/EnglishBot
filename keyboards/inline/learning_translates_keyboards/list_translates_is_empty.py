from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_data import repeat_translate_callback
from keyboards.inline.buttons.add_translate import add_translate_button
from loader import _

empty_translates_keyboard = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [
            add_translate_button,
            InlineKeyboardButton(text=_("🔁Повторять слова"),
                                 callback_data=repeat_translate_callback.new(
                                     is_selected='True'))
        ]
    ]
)
