from aiogram.types import Message, ReplyKeyboardRemove, CallbackQuery

from loader import dp, _

from keyboards.inline.callback_data import settings_callback


@dp.callback_query_handler(settings_callback.filter(settings_item="instruction"))
async def show_instruction(call: CallbackQuery):
    await call.answer(cache_time=5)
    await call.message.answer(_("<i>ИНСТРУКЦИЯ</i>\n\n"
                                "Как и в реальной жизни, слова, которые мы изучаем, должны быть где-то записаны.\n"
                                "Для этого и существуют СЛОВАРИ. Так что первым делом нужно создать словарь\n"
                                "   <b>1. Создать словарь</b>\n"
                                "В самом начале я тебе помог создать первый словарь, "
                                "но ты можешь создать несколько словарей, "
                                "чтобы например <i>учить два разных языка</i>, "
                                "либо <i>учить слова по разным категориям</i>.\n"
                                "Но подробнее как учить эффективно в РЕКОМЕНДАЦИЯХ\n"
                                "Дальше ты создаешь свои переводы\n"
                                "   <b>2. Создать перевод</b>\n"
                                "То есть ты записываешь слово и к нему пишешь перевод на любом языке. "
                                "Рекомендую создавать в день не меньше 5 слов!\n"
                                "Я, кстати, буду тебе об этом напоминать. "
                                "Например, когда ты добавишь всего 3 слова и начнешь \n"
                                "   <b>3. Учить</b>\n"
                                "Частично логика подбора переводов сделана на основе графика Эббингауза.\n"
                                "Но саму суть лучше покажет вот эта картинка:"))

    photo_file_id = 'AgACAgIAAxkBAAIqxl_TknrS85hLkQcx6R-bavEeiD-' \
                    'TAALIrzEbuvWYSv7SS_RabX6UDAFFli4AAwEAAwIAA3kAA-ORBQABHgQ'
    await call.message.answer_photo(photo_file_id, caption=_('*Время взято от последнего повторения*'))
