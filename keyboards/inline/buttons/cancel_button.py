from aiogram.types import InlineKeyboardButton
from keyboards.inline.callback_data import cancel_button_callback
from loader import _

cancel_button = InlineKeyboardButton(text=_("Отменить 🚫"),
                                     callback_data=cancel_button_callback.new(
                                         state='True'
                                     ))
