from aiogram.dispatcher.filters import Text

from aiogram.types import Message
from loader import dp, db, _


@dp.message_handler(Text("🎯Учить"))
async def checking_new_translates(message: Message):
    await message.answer(_("Выбрано учить"))
    tg_id = message.from_user.id

    current_dictionary = await db.select_current_dictionary(tg_id)
    learning_translates = await db.select_learning_translates(current_dictionary)
    print(learning_translates)