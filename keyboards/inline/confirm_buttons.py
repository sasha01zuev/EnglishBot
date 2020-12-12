from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_data import confirm_callback

confirm_keyboard = InlineKeyboardMarkup(row_width=1,
                                        inline_keyboard=[
                                            [
                                                InlineKeyboardButton(text="Подтвердить ✅",
                                                                     callback_data=confirm_callback.new(
                                                                         item="accept")),
                                                InlineKeyboardButton(text="Отмена 🚫",
                                                                     callback_data=confirm_callback.new(
                                                                         item="cancel"))
                                            ]

                                        ]
                                        )
