from aiogram.types import InlineKeyboardButton
from keyboards.inline.callback_data import add_translate_callback
from loader import _

add_translate_button = InlineKeyboardButton(text=_("📌Добавить перевод"),
                                            callback_data=add_translate_callback.new(
                                                is_selected='True'
                                            ))
