from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_data import start_learning_callback
from keyboards.inline.buttons.add_translate import add_translate_button

shortage_translates_keyboard = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [
            add_translate_button,
            InlineKeyboardButton(text="🔁Учить оставшиеся",
                                 callback_data=start_learning_callback.new(
                                     is_selected='True'))
        ]
    ]
)
