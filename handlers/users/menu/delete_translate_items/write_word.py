from aiogram.types import CallbackQuery, ReplyKeyboardRemove, Message
from aiogram.dispatcher import FSMContext

from keyboards.inline.delete_translate_buttons import delete_translate_callback, delete_translate_keyboard
from keyboards.inline.confirm_buttons import confirm_keyboard, confirm_callback
from loader import dp
from states.delete_inputted_translate import DeleteInputtedTranslate


@dp.callback_query_handler(delete_translate_callback.filter(item="write_word"))
async def write_word(call: CallbackQuery, callback_data: dict):
    await call.answer(cache_time=5)
    deletion_type = callback_data['item']
    await call.message.answer(f"Введи название словаря")
    # await call.message.edit_reply_markup()
    await DeleteInputtedTranslate.InputWord.set()


@dp.message_handler(state=DeleteInputtedTranslate.InputWord)
async def check_deletion(message: Message, state: FSMContext):
    await state.update_data(dict_name=message.text)
    await message.answer(f'Вы действительно хотите удалить "{message.text}"?', reply_markup=confirm_keyboard)


@dp.callback_query_handler(confirm_callback.filter(item="accept"), state=DeleteInputtedTranslate.InputWord)
async def accept_deletion(call: CallbackQuery, callback_data: dict, state: FSMContext):
    data = await state.get_data()
    dict_name = data.get("dict_name")
    await call.message.answer(f'Принято. Удаление "{dict_name}"...')
    await state.finish()
