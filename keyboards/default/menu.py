from aiogram.types import ReplyKeyboardMarkup, KeyboardButton
from loader import _

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text=_("Новый перевод")),
            KeyboardButton(text=_("Удалить перевод"))
        ],
        [
            KeyboardButton(text=_("Новый словарь")),
            KeyboardButton(text=_("Поменять словарь")),
            KeyboardButton(text=_("Удалить словарь"))
        ],
        [
            KeyboardButton(text=_("Настройки"))
        ]
    ],
    resize_keyboard=True
)
