from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ReplyKeyboardRemove

from aiogram.dispatcher import FSMContext
from states import CreateNewDict

from keyboards.default import menu
from loader import dp, db, _


@dp.message_handler(Text("📓Новый словарь"))
async def new_dictionary(message: Message):
    dictionaries = await db.select_dictionaries(message.from_user.id)
    if len(dictionaries) == 10:
        await message.answer(_("Вы не можете создать больше 10 словарей!"))
    else:
        await message.answer(_("Напиши название своего словаря"), reply_markup=ReplyKeyboardRemove())
        await CreateNewDict.SetDictionaryName.set()


@dp.message_handler(state=CreateNewDict.SetDictionaryName)
async def set_dictionary_name(message: Message, state: FSMContext):
    await state.update_data(dictionary_name=message.text)
    data = await state.get_data()
    dictionary_name = data.get("dictionary_name")
    tg_id = message.from_user.id

    ########################################################################
    #                           DATABASE Query                             #
    await db.add_dictionary(tg_id, dictionary_name)
    #                                                                      #
    ########################################################################

    await message.answer(_('Вы создали новый словарь "{dictionary_name}"').format(
        dictionary_name=dictionary_name
    ), reply_markup=menu)
    await state.finish()
