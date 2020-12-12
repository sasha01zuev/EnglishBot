from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="🎯Учить")
        ],
        [
            KeyboardButton(text="📌Новый перевод"),
            KeyboardButton(text="🗑Удалить перевод")
        ],
        [
            KeyboardButton(text="📓Новый словарь"),
            KeyboardButton(text="Поменять словарь"),
            KeyboardButton(text="🗑Удалить словарь")
        ],
        [
            KeyboardButton(text="⚙Настройки")
        ]
    ],
    resize_keyboard=True
)
