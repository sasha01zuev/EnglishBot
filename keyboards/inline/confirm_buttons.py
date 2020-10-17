from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_data import confirm_callback
from loader import _

confirm_keyboard = InlineKeyboardMarkup(row_width=1,
                                        inline_keyboard=[
                                            [
                                                InlineKeyboardButton(text=_("Подтвердить ✅"),
                                                                     callback_data=confirm_callback.new(
                                                                         item="accept")),
                                                InlineKeyboardButton(text=_("Отмена 🚫"),
                                                                     callback_data=confirm_callback.new(
                                                                         item="cancel"))
                                            ]

                                        ]
                                        )
