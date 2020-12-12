from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline.callback_data import learning_response_callback
from loader import dp, db
from keyboards.inline.learning_translates_keyboards.check_show_translate_response import check_show_translate_keyboard
from states import ChooseResponse


@dp.callback_query_handler(learning_response_callback.filter(is_selected="show_translate"),
                           state=ChooseResponse.SetChooseResponse)
async def show_translate(call: CallbackQuery, callback_data: dict, state: FSMContext):

    await call.answer()
    await call.message.delete()
    print('show here')
    data = await state.get_data()
    english_word = data.get("english_word")
    russian_word = data.get("russian_word")
    translate_id = data.get("translate_id")
    dictionary_id = data.get("dictionary_id")

    await call.message.answer(f'{english_word} - {russian_word}', reply_markup=check_show_translate_keyboard)
    ########################################################################
    #                        DATABASE Queries                              #

    ########################################################################
    await ChooseResponse.SetChooseResponse.set()
