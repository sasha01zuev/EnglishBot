from aiogram.dispatcher.filters import Text

from aiogram.types import Message
from loader import dp, db, _


@dp.message_handler(Text("🎯Учить"))
async def checking_new_translates(message: Message):
    await message.answer(_("Выбрано учить"))
    tg_id = message.from_user.id

    current_dictionary = await db.select_current_dictionary(tg_id)
    learning_translates = await db.select_learning_translates(current_dictionary)

    # TODO. Check date of learning translates.
    #  IF there is not today's translates -- show message and suggest adding
    #  new translates or learn remaining
    #  ELIF today's translates -- if translates more than 3 - start learn
    #                             else suggest to add new translates
    #  ELIF list for learning translate is empty -- suggest to add new translates
    #                                               or
    #                                               repeat translates

    print(learning_translates)
