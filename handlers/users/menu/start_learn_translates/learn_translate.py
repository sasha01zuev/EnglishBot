import datetime
import random

from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import Message, CallbackQuery

from keyboards.inline.callback_data import start_learning_callback
from keyboards.inline.learning_translates_keyboards import \
    shortage_translates_keyboard, empty_translates_keyboard, past_translates_keyboard, check_response_keyboard
from loader import dp, db
from states import ChooseResponse


@dp.message_handler(Text("🎯Учить"))
async def checking_new_translates(message: Message, state: FSMContext):
    """Checking date of learning translates.

    IF there is not today's translates -- show message and suggest adding new translates or learn remaining
    ELIF today's translate < 4:
        IF past translates > 0 -- show unlocked translates from past and today's translates,
    and suggest adding new translates or learn remaining
        ELSE -- show today's translates and suggest to add new translates or learn remaining
    ELSE -- Main logic of selection translates from db for learning

    """

    user_id = message.from_user.id

    current_date = datetime.date.today()
    current_day = current_date.day
    current_year = current_date.year
    current_month = current_date.month

    todays_words_quantity = 0

    #############################################################################
    #                        DATABASE Queries                                   #
    current_dictionary = await db.select_current_dictionary(user_id)
    learning_translates = await db.select_learning_translates(current_dictionary)
    quantity_of_available_translates = len(await db.learning_translates_id(current_dictionary))
    #############################################################################

    for translate in learning_translates:
        if (translate[2].year, translate[2].month, translate[2].day) == (current_year, current_month, current_day):
            """If date of translate coincide with current date - increment todays_words_quantity"""
            todays_words_quantity += 1

    if len(learning_translates) == 0:
        """Show message and suggest adding new translates or learn remaining"""
        await message.answer('Нету добавленных переводов на изучение!', reply_markup=empty_translates_keyboard)
    elif todays_words_quantity < 4:
        if quantity_of_available_translates > 0:
            """
            Show unlocked translates from past and today's translates, 
            and suggest adding new translates or learn remaining
            """
            await message.answer(f"У вас остались переводы с прошлых дней.\n"
                                 f"Количество: {quantity_of_available_translates}\n"
                                 f"Количество сегодняшних переводов: {todays_words_quantity}.",
                                 reply_markup=past_translates_keyboard)
        else:
            """Show today's translates and suggest to add new translates or learn remaining"""
            await message.answer(f"Количество сегодняшних переводов: {todays_words_quantity}. "
                                 f"Рекомендуем добавить еще!",
                                 reply_markup=shortage_translates_keyboard)

    else:
        """Redirect to main logic for learning translates"""
        user_id = message.from_user.id

        ################################################################################
        #                             DATABASE Queries                                 #
        current_dictionary = await db.select_current_dictionary(user_id)
        translates = await db.learning_translates_id(current_dictionary)  # Fetch available translates
        translate_values = [x[0] for x in translates]    # Fetch ID's from available translates
        random_translate_id = random.choice(translate_values)   # Random choice from ID's
        translate = await db.translate_info(random_translate_id)    # Fetch translate row of random available ID
        ################################################################################

        translate_id = random_translate_id
        english_word = translate[1]
        russian_word = translate[2]
        dictionary_id = translate[3]

        await message.answer(f'{english_word} - ?', reply_markup=check_response_keyboard)  # Translation knowledge test
        await ChooseResponse.SetChooseResponse.set()
        await state.update_data(english_word=english_word, russian_word=russian_word, translate_id=translate_id,
                                dictionary_id=dictionary_id)


@dp.callback_query_handler(start_learning_callback.filter(is_selected='True'))
async def learning_process(call: CallbackQuery, state: FSMContext):
    """Main logic of selection translates from db for learning. But for callback!"""
    await call.answer()
    await call.message.delete()
    user_id = call.from_user.id
    iteration = True

    while iteration:
        """Cycle for checking for non-repetition with previous translate. 
        
        Every time it must be unique IF there more than 1 available translate!
        """
        try:
            ################################################################################
            #                             DATABASE Queries                                 #
            current_dictionary = await db.select_current_dictionary(user_id)
            translates = await db.learning_translates_id(current_dictionary)  # Fetch available translates
            translate_values = [x[0] for x in translates]    # Fetch ID's from available translates
            random_translate_id = random.choice(translate_values)    # Random choice from ID's
            translate = await db.translate_info(random_translate_id)    # Fetch translate row of random available ID
            previous_translate_id = await db.select_last_learning_translate_id(user_id)
            ################################################################################

            if len(translates) == 1:
                """Checking for the previous element is not done because only 1 available translate"""
                translate_id = random_translate_id
                english_word = translate[1]
                russian_word = translate[2]
                dictionary_id = translate[3]

                await call.message.answer(f'{english_word} - ?', reply_markup=check_response_keyboard)  # Test
                await ChooseResponse.SetChooseResponse.set()
                await state.update_data(english_word=english_word, russian_word=russian_word,
                                        translate_id=translate_id, dictionary_id=dictionary_id)
                await db.set_last_learning_translate_id(user_id, translate_id)
                iteration = False    # Stop cycle
            elif random_translate_id == previous_translate_id:
                """If current translate equals previous translate - repeat cycle"""
                pass    # Cycle is continued
            else:
                """Current translate != prev translate and that's why - Translation knowledge test"""
                translate_id = random_translate_id
                english_word = translate[1]
                russian_word = translate[2]
                dictionary_id = translate[3]

                await call.message.answer(f'{english_word} - ?', reply_markup=check_response_keyboard)
                await ChooseResponse.SetChooseResponse.set()
                await state.update_data(english_word=english_word, russian_word=russian_word, translate_id=translate_id,
                                        dictionary_id=dictionary_id)
                await db.set_last_learning_translate_id(user_id, translate_id)
                iteration = False    # Stop cycle
        except IndexError:
            """If it raised - available translates list is empty"""
            await call.message.answer("Нету переводов на заучивание!")
            iteration = False    # Stop cycle
        except Exception as error:
            """If it raised - unknown error!"""
            await call.message.answer("Неизвестная ошибка")
            print(error)
            iteration = False     # Stop cycle
