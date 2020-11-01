from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_data import learn_remaining_callback
from keyboards.inline.buttons.add_translate import add_translate_button
from loader import _

past_translates_keyboard = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [
            add_translate_button,
            InlineKeyboardButton(text=_("🔁Учить оставшиеся"),
                                 callback_data=learn_remaining_callback.new(
                                     is_selected='True'))
        ]
    ]
)
