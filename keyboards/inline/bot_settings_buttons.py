from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from keyboards.inline.callback_data import settings_callback


bot_settings = InlineKeyboardMarkup(row_width=1,
                                    inline_keyboard=[
                                        [
                                            InlineKeyboardButton(text="Обратить перевод 🔁",
                                                                 callback_data=settings_callback.new(
                                                                     settings_item="reverse_translate",
                                                                     setting_choose=False))
                                        ],

                                        [
                                            InlineKeyboardButton(text="Поменять язык - 🇺🇸",
                                                                 callback_data=settings_callback.new(
                                                                  settings_item="change_language",
                                                                     setting_choose="ru"))
                                        ]

                                    ]
                                    )
