from aiogram.dispatcher.filters import Text
from aiogram.types import Message, ReplyKeyboardRemove

from aiogram.dispatcher import FSMContext
from states.create_new_dicitonary import CreateNewDict

from keyboards.default import menu
from loader import dp



@dp.message_handler(Text("Новый словарь"))
async def new_dictionary(message: Message):
    await message.answer("Напиши название своего словаря", reply_markup=ReplyKeyboardRemove())
    await CreateNewDict.SetDictionaryName.set()


@dp.message_handler(state=CreateNewDict.SetDictionaryName)
async def set_dictionary_name(message: Message, state: FSMContext):
    await state.update_data(dictionary_name=message.text)
    data = await state.get_data()
    dictionary_name = data.get("dictionary_name")
    await message.answer(f'Вы создали новый словарь под назанием "{dictionary_name}"', reply_markup=menu)
    await state.finish()
