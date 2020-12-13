from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline.callback_data import learning_response_callback
from keyboards.inline.learning_translates_keyboards import check_continuation_learning_keyboard
from loader import dp, db
from states import ChooseResponse


@dp.callback_query_handler(learning_response_callback.filter(is_selected="know"),
                           state=ChooseResponse.SetChooseResponse)
async def know_translate(call: CallbackQuery,  state: FSMContext):
    """Checking stage of translate, updating translate and checking continuation of learning"""
    await call.answer()
    await call.message.delete()

    data = await state.get_data()
    translate_id = data.get("translate_id")
    dictionary_id = data.get("dictionary_id")

    ########################################################################
    #                        DATABASE Queries                              #
    repetition_number = await db.check_repetition_number(translate_id)  # Stage of translate
    await db.update_translate(translate_id, dictionary_id, repetition_number)  # Updating translate
    ########################################################################

    await call.message.answer("Учим дальше?", reply_markup=check_continuation_learning_keyboard)
    await state.finish()
