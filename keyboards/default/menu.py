from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


menu = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="Добавить слово в словарь"),
            KeyboardButton(text="Поменять словарь")
        ],
        [
            KeyboardButton(text="Создать словарь"),
            KeyboardButton(text="Удалить словарь")
        ],
        [
            KeyboardButton(text="Настройки")
        ]
    ],
    # resize_keyboard=True
)