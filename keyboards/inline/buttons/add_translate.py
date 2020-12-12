from aiogram.types import InlineKeyboardButton
from keyboards.inline.callback_data import add_translate_callback

add_translate_button = InlineKeyboardButton(text="📌Добавить перевод",
                                            callback_data=add_translate_callback.new(
                                                is_selected='True'
                                            ))
