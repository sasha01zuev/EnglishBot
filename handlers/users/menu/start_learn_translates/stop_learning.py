from aiogram.dispatcher import FSMContext
from aiogram.types import CallbackQuery

from keyboards.inline.callback_data import start_learning_callback
from loader import dp


@dp.callback_query_handler(start_learning_callback.filter(is_selected='False'))
async def stop_learning(call: CallbackQuery, state: FSMContext):
    await call.answer()
    await call.message.delete()
    await call.message.answer("Обучение остановлено!")
    await state.finish()
