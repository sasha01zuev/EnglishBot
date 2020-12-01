from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline.learning_translates_keyboards import check_continuation_learning_keyboard
from keyboards.inline.callback_data import learning_response_callback
from loader import dp, db, _
from states import ChooseResponse


@dp.callback_query_handler(learning_response_callback.filter(is_selected="unknow"),
                           state=ChooseResponse.SetChooseResponse)
async def unknow_translate(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer()
    await call.message.delete()

    data = await state.get_data()
    english_word = data.get("english_word")
    russian_word = data.get("russian_word")
    # translate_id = data.get("translate_id")
    # dictionary_id = data.get("dictionary_id")

    await call.message.answer(_("{english} - {russian}").format(english=english_word, russian=russian_word),
                              reply_markup=check_continuation_learning_keyboard)
    # await call.message.answer(_("Учим дальше?"))

    await state.finish()


@dp.callback_query_handler(learning_response_callback.filter(is_selected="showed_unknow"),
                           state=ChooseResponse.SetChooseResponse)
async def unknow_translate(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer()
    await call.message.delete()

    await call.message.answer(_("Учим дальше?"), reply_markup=check_continuation_learning_keyboard)
    # await call.message.answer(_("Учим дальше?"))

    await state.finish()