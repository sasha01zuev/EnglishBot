from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline.callback_data import learning_response_callback
from keyboards.inline.learning_translates_keyboards.check_show_translate_response import check_show_translate_keyboard
from loader import dp
from states import ChooseResponse


@dp.callback_query_handler(learning_response_callback.filter(is_selected="show_translate"),
                           state=ChooseResponse.SetChooseResponse)
async def show_translate(call: CallbackQuery, state: FSMContext):
    """Showing full translate and check user answer:  knew or didn't know"""
    await call.answer()
    await call.message.delete()

    data = await state.get_data()
    english_word = data.get("english_word")
    russian_word = data.get("russian_word")

    await call.message.answer(f'{english_word} - {russian_word}', reply_markup=check_show_translate_keyboard)
    await ChooseResponse.SetChooseResponse.set()
