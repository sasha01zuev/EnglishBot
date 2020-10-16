from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_data import settings_callback
from loader import _


bot_settings = InlineKeyboardMarkup(row_width=1,
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(text=_("Обратить перевод 🔁"),
                                                                 callback_data=settings_callback.new(
                                                                     settings_item="reverse_translate"))
                                        ],

                                        [
                                            InlineKeyboardButton(text=_("Поменять язык - 🇺🇸"),
                                                                 callback_data=settings_callback.new(
                                                                  settings_item="change_language"))
                                        ]

                                    ]
                                    )
