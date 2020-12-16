from aiogram.dispatcher.filters import Command
from aiogram.types import CallbackQuery, Message

from keyboards.inline.callback_data import settings_callback
from loader import dp


@dp.callback_query_handler(settings_callback.filter(settings_item="recommendation"))
async def show_recommendations(call: CallbackQuery):
    """Show recommendation for user"""
    await call.answer(cache_time=5)
    await call.message.delete()
    await call.message.answer('<i>РЕКОМЕНДАЦИИ</i>\n\n'
                              'Чтобы эффективно учить новые слова, рекомендую прочитать несколько советов ниже!\n\n'
                              '<b>1. Объединяйте слова по тематике</b>\n'
                              'Как легко запомнить английские слова? Обычно хорошо запоминаются группы слов, '
                              'относящиеся к одной теме. Поэтому старайтесь разбить слова '
                              'на группы по 5-10 штук и учить их.')
    photo_file_id = 'AgACAgIAAxkBAAMdX9pOo-4VZiYhKoW-VLM8Z-zeyFMAAlCxMRu1ld' \
                    'BKyaKqlqhaqZuO5GybLgADAQADAgADeAADIWcAAh4E'
    await call.message.answer_photo(photo_file_id)  # Send picture

    await call.message.answer('<b>2. Используйте ассоциации и персонализацию</b>\n'
                              'Этот способ любят многие студенты: чтобы выучить какое-то слово, '
                              'нужно придумать ассоциацию на русском языке. '
                              'Например, необходимо запомнить слово obstinacy (упрямство). '
                              'Разбейте его на три слога: ob-stin-acy, получится «упрямый, как об-стену-осел».\n\n'
                              '<b>3. Используйте изученную лексику в речи</b>\n'
                              'Как правильно учить английские слова и не забывать их? '
                              'Вы знакомы с принципом use it or lose it? '
                              'Чтобы знания остались в памяти, нужно активно «юзать» их. '
                              'Хорошая практика — составлять короткие рассказы с использованием новых слов.\n\n'
                              '<b>4. Выполняйте свой ежедневный план</b>\n'
                              'Для среднестатистического человека лучше всего учить 5-10 слов в день. '
                              'Четко следуйте своему плану изучения новой лексики, чтобы увидеть прогресс.\n\n'
                              '<b>5. Занимайтесь регулярно</b>\n'
                              'Только при постоянной равномерной нагрузке ваш мозг будет усваивать все знания.\n\n'
                              '<b>6. Нагрузка при обучении должна соответствовать вашим потребностям</b>\n'
                              'Дайте мозгу отдых: учите иностранный язык в спокойном темпе, '
                              'подходящем именно вам. Не обращайте внимания на соседку Люсю, '
                              'которая благодаря новой «голливудской» методике '
                              'освоила азы языка за два 3-часовых урока.\n\n'
                              '<b>7. Одно слово - два значения</b>\n'
                              'Нужно посмотреть не используется ли ваше слово в двух разных значениях. '
                              'Например: milk - молоко, to milk - доить. '
                              'Ведь так мы за раз выучили уже два слова, а не одно')


@dp.message_handler(Command('recommendations'))
async def show_recommendations(message: Message):
    """Show recommendation for user"""
    await message.delete()
    await message.answer('<i>РЕКОМЕНДАЦИИ</i>\n\n'
                         'Чтобы эффективно учить новые слова, рекомендую прочитать несколько советов ниже!\n\n'
                         '<b>1. Объединяйте слова по тематике</b>\n'
                         'Как легко запомнить английские слова? Обычно хорошо запоминаются группы слов, '
                         'относящиеся к одной теме. Поэтому старайтесь разбить слова '
                         'на группы по 5-10 штук и учить их.')
    photo_file_id = 'AgACAgIAAxkBAAMdX9pOo-4VZiYhKoW-VLM8Z-zey' \
                    'FMAAlCxMRu1ldBKyaKqlqhaqZuO5GybLgADAQADAgADeAADIWcAAh4E'
    await message.answer_photo(photo_file_id)  # Send picture

    await message.answer('<b>2. Используйте ассоциации и персонализацию</b>\n'
                         'Этот способ любят многие студенты: чтобы выучить какое-то слово, '
                         'нужно придумать ассоциацию на русском языке. '
                         'Например, необходимо запомнить слово obstinacy (упрямство). '
                         'Разбейте его на три слога: ob-stin-acy, получится «упрямый, как об-стену-осел».\n\n'
                         '<b>3. Используйте изученную лексику в речи</b>\n'
                         'Как правильно учить английские слова и не забывать их? '
                         'Вы знакомы с принципом use it or lose it? '
                         'Чтобы знания остались в памяти, нужно активно «юзать» их. '
                         'Хорошая практика — составлять короткие рассказы с использованием новых слов.\n\n'
                         '<b>4. Выполняйте свой ежедневный план</b>\n'
                         'Для среднестатистического человека лучше всего учить 5-10 слов в день. '
                         'Четко следуйте своему плану изучения новой лексики, чтобы увидеть прогресс.\n\n'
                         '<b>5. Занимайтесь регулярно</b>\n'
                         'Только при постоянной равномерной нагрузке ваш мозг будет усваивать все знания.\n\n'
                         '<b>6. Нагрузка при обучении должна соответствовать вашим потребностям</b>\n'
                         'Дайте мозгу отдых: учите иностранный язык в спокойном темпе, '
                         'подходящем именно вам. Не обращайте внимания на соседку Люсю, '
                         'которая благодаря новой «голливудской» методике '
                         'освоила азы языка за два 3-часовых урока.\n\n'
                         '<b>7. Одно слово - два значения</b>\n'
                         'Нужно посмотреть не используется ли ваше слово в двух разных значениях. '
                         'Например: milk - молоко, to milk - доить. '
                         'Ведь так мы за раз выучили уже два слова, а не одно')
