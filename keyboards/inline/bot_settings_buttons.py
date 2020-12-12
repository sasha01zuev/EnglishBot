from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_data import settings_callback

bot_settings = InlineKeyboardMarkup(row_width=1,
                                    inline_keyboard=[

                                        [
                                            InlineKeyboardButton(text="Обратить перевод 🔁",
                                                                 callback_data=settings_callback.new(
                                                                     settings_item="reverse_translate"))
                                        ],
                                        [
                                            InlineKeyboardButton(text="Рекомендации ✅",
                                                                 callback_data=settings_callback.new(
                                                                     settings_item="recommendation"
                                                                 ))
                                        ],
                                        [
                                            InlineKeyboardButton(text="Полная инструкция 📄",
                                                                 callback_data=settings_callback.new(
                                                                     settings_item="instruction"
                                                                 ))
                                        ]

                                    ]
                                    )
