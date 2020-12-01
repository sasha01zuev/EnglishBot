from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from aiogram.types import Message, CallbackQuery, InlineKeyboardButton
from loader import dp, db, _
from keyboards.inline.learning_translates_keyboards import \
    shortage_translates_keyboard, empty_translates_keyboard, past_translates_keyboard, check_response_keyboard
import datetime
from keyboards.inline.callback_data import start_learning_callback, show_translate_callback
from states import StartLearningTranslates, ChooseResponse


@dp.message_handler(Text(_("🎯Учить")))
async def checking_new_translates(message: Message):
    tg_id = message.from_user.id

    current_dictionary = await db.select_current_dictionary(tg_id)
    learning_translates = await db.select_learning_translates(current_dictionary)

    # Check date of learning translates.
    #  IF there is not today's translates -- show message and suggest adding
    #  new translates or learn remaining
    #  ELIF today's translates -- if translates more than 3 - suggest to start learn
    #                             else suggest to add new translates
    #  ELIF list for learning translate is empty -- suggest to add new translates
    #                                               or
    #                                               repeat translates

    current_date = datetime.date.today()
    current_day = current_date.day
    current_year = current_date.year
    current_month = current_date.month

    todays_words_quantity = 0
    past_translates = 0

    for translate in learning_translates:
        if (translate[2].year, translate[2].month, translate[2].day) == (current_year, current_month, current_day):
            todays_words_quantity += 1
        elif (translate[2].year, translate[2].month, translate[2].day) != (current_year, current_month, current_day):
            past_translates += 1

    print("Quantity: ", todays_words_quantity)

    if len(learning_translates) == 0:
        await message.answer(_('Нету добавленых переводов!'), reply_markup=empty_translates_keyboard)
    elif todays_words_quantity < 4:
        await message.answer(_("Количетсво переводов: {quantity}. "
                               "Рекомендуем добавить еще!").format(quantity=todays_words_quantity),
                             reply_markup=shortage_translates_keyboard)
    elif todays_words_quantity == 0 and past_translates > 0:
        await message.answer(_("У вас остались переводы на заучиваение с прошлых дней.\n"
                               "Количество: {quantity}").format(quantity=past_translates),
                             reply_markup=past_translates_keyboard)
    else:
        # Redirect to main logic for learning translates
        pass


@dp.callback_query_handler(start_learning_callback.filter(is_selected='True'))
async def learning_process(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer()
    await call.message.delete()
    tg_id = call.from_user.id

    ################################################################################
    #                             DATABASE Queries                                 #
    current_dictionary = await db.select_current_dictionary(tg_id)
    random_translate = await db.select_random_learning_translate(current_dictionary)
    ################################################################################

    translate_id = random_translate[0]
    english_word = random_translate[1]
    russian_word = random_translate[2]
    dictionary_id = random_translate[3]

    await call.message.answer(f'{english_word} - ?', reply_markup=check_response_keyboard)

    await ChooseResponse.SetChooseResponse.set()
    await state.update_data(english_word=english_word, russian_word=russian_word, translate_id=translate_id,
                            dictionary_id=dictionary_id)
