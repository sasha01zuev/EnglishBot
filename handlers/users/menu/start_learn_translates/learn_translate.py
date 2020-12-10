import datetime
import random

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

from keyboards.inline.callback_data import start_learning_callback
from keyboards.inline.learning_translates_keyboards import \
    shortage_translates_keyboard, empty_translates_keyboard, past_translates_keyboard, check_response_keyboard
from loader import dp, db, _
from states import ChooseResponse


@dp.message_handler(Text(_("🎯Учить")))
async def checking_new_translates(message: Message, state: FSMContext):
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
        if past_translates > 0:
            await message.answer(_("У вас остались переводы на заучиваение с прошлых дней.\n"
                                   "Количество: {past_translates}\n"
                                   "Количетсво сегодняшних переводов: {todays_translates}.").format(
                past_translates=past_translates, todays_translates=todays_words_quantity),
                reply_markup=past_translates_keyboard)
        else:
            await message.answer(_("Количетсво сегодняшних переводов: {quantity}. "
                                   "Рекомендуем добавить еще!").format(quantity=todays_words_quantity),
                                 reply_markup=shortage_translates_keyboard)

    else:
        # Redirect to main logic for learning translates
        tg_id = message.from_user.id

        ################################################################################
        #                             DATABASE Queries                                 #
        current_dictionary = await db.select_current_dictionary(tg_id)
        random_translate = await db.select_random_learning_translate(current_dictionary)
        translates = await db.learning_translates(current_dictionary)
        translate_values = [x[0] for x in translates]
        random_translate_id = random.choice(translate_values)
        translate = await db.translate_info(random_translate_id)
        ################################################################################

        translate_id = random_translate_id
        english_word = translate[1]
        russian_word = translate[2]
        dictionary_id = translate[3]
        # Stopped here!!!!
        await message.answer(f'{english_word} - ?', reply_markup=check_response_keyboard)
        await ChooseResponse.SetChooseResponse.set()
        await state.update_data(english_word=english_word, russian_word=russian_word, translate_id=translate_id,
                                dictionary_id=dictionary_id)


@dp.callback_query_handler(start_learning_callback.filter(is_selected='True'))
async def learning_process(call: CallbackQuery, callback_data: dict, state: FSMContext):
    await call.answer()
    await call.message.delete()
    tg_id = call.from_user.id

    current_dictionary = await db.select_current_dictionary(tg_id)
    learning_translates = await db.select_learning_translates(current_dictionary)

    iteration = True

    while iteration:
        try:
            ################################################################################
            #                             DATABASE Queries                                 #
            current_dictionary = await db.select_current_dictionary(tg_id)
            translates = await db.learning_translates(current_dictionary)
            translate_values = [x[0] for x in translates]
            random_translate_id = random.choice(translate_values)
            # random_translate = await db.select_random_learning_translate(current_dictionary)
            translate = await db.translate_info(random_translate_id)
            previous_translate = await db.select_last_learning_translate_id(tg_id)
            ################################################################################
            print(previous_translate)

            if len(translates) == 1:
                translate_id = random_translate_id
                english_word = translate[1]
                russian_word = translate[2]
                dictionary_id = translate[3]
                # Stopped here!!!!
                await call.message.answer(f'{english_word} - ?', reply_markup=check_response_keyboard)

                await ChooseResponse.SetChooseResponse.set()
                await state.update_data(english_word=english_word, russian_word=russian_word, translate_id=translate_id,
                                        dictionary_id=dictionary_id)
                await db.set_last_learning_translate_id(tg_id, translate_id)
                iteration = False
            elif random_translate_id == previous_translate:
                pass
            else:
                translate_id = random_translate_id
                english_word = translate[1]
                russian_word = translate[2]
                dictionary_id = translate[3]
                # Stopped here!!!!
                await call.message.answer(f'{english_word} - ?', reply_markup=check_response_keyboard)

                await ChooseResponse.SetChooseResponse.set()
                await state.update_data(english_word=english_word, russian_word=russian_word, translate_id=translate_id,
                                        dictionary_id=dictionary_id)
                await db.set_last_learning_translate_id(tg_id, translate_id)
                iteration = False
        except IndexError:
            await call.message.answer(_("Нету переводов на заучивание!"))
            iteration = False
        except Exception as error:
            await call.message.answer(_("Неизвестная ошибка"))
            print(error)
            iteration = False
