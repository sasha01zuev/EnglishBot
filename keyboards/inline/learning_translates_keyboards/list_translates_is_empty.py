from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_data import repeat_translate_callback, start_learning_callback
from keyboards.inline.buttons.add_translate import add_translate_button

empty_translates_keyboard = InlineKeyboardMarkup(
    row_width=1,
    inline_keyboard=[
        [
            add_translate_button,
            InlineKeyboardButton(text="🔁Повторять слова",
                                 callback_data=start_learning_callback.new(
                                     is_selected='True'))
        ]
    ]
)
