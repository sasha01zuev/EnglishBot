from aiogram.types import InlineKeyboardButton
from keyboards.inline.callback_data import cancel_button_callback

cancel_button = InlineKeyboardButton(text="Отменить 🚫",
                                     callback_data=cancel_button_callback.new(
                                         state='True'
                                     ))
