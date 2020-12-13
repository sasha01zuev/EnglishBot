from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ReplyKeyboardRemove

from keyboards.default import menu
from loader import dp, db
from states import CreateNewDict


@dp.message_handler(Text("📓Новый словарь"))
async def new_dictionary(message: Message):
    """Check quantity of user dictionaries"""
    dictionaries = await db.select_dictionaries(message.from_user.id)
    if len(dictionaries) == 10:  # Limit in 10 dictionaries for user
        await message.answer("Вы не можете создать больше 10 словарей!")
    else:  # Available to add one more dictionaries
        await message.answer("Напиши название своего словаря", reply_markup=ReplyKeyboardRemove())
        await CreateNewDict.SetDictionaryName.set()


@dp.message_handler(state=CreateNewDict.SetDictionaryName)
async def set_dictionary_name(message: Message, state: FSMContext):
    """Add new dictionary to database"""
    await state.update_data(dictionary_name=message.text)
    data = await state.get_data()
    dictionary_name = data.get("dictionary_name")
    user_id = message.from_user.id

    ########################################################################
    #                           DATABASE Query                             #
    await db.add_dictionary(user_id, dictionary_name)
    ########################################################################

    await message.answer(f'Вы создали новый словарь "{dictionary_name}"', reply_markup=menu)
    await state.finish()
