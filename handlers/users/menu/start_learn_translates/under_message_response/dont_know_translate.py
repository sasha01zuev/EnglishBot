from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline.learning_translates_keyboards import check_continuation_learning_keyboard
from keyboards.inline.callback_data import learning_response_callback
from loader import dp
from states import ChooseResponse


@dp.callback_query_handler(learning_response_callback.filter(is_selected="unknow"),
                           state=ChooseResponse.SetChooseResponse)
async def unknown_translate(call: CallbackQuery, state: FSMContext):
    """Show translate and check continuation of learning"""
    await call.answer()
    await call.message.delete()
    data = await state.get_data()
    english_word = data.get("english_word")
    russian_word = data.get("russian_word")

    await call.message.answer(f"{english_word} - {russian_word}",
                              reply_markup=check_continuation_learning_keyboard)
    await state.finish()


@dp.callback_query_handler(learning_response_callback.filter(is_selected="showed_unknow"),
                           state=ChooseResponse.SetChooseResponse)
async def showed_unknown_translate(call: CallbackQuery, state: FSMContext):
    """Checking continuation of learning"""
    await call.answer()
    await call.message.delete()
    await call.message.answer("Учим дальше?", reply_markup=check_continuation_learning_keyboard)
    await state.finish()
