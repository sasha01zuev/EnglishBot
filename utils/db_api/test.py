import asyncio
import random
from utils.db_api.postgresql import Database


async def test():
    """Test for working with database queries"""
    # await db.add_translate(2, 'english_word', 'russian_word')

    # select_dict_for_start = await db.select_dictionary_for_start(609200395)
    # print(select_dict_for_start)

    # select_dictionaries = await db.select_dictionaries(609200395)
    # print(select_dictionaries)
    # print(select_dictionaries[0][1])
    # print([[name[0], name[1]] for name in select_dictionaries])

    # current_dictionary = await db.select_current_dictionary(609200395)
    # print(current_dictionary)
    # translate = await db.select_translate(current_dictionary, word='fak')
    # print(translate)

    # last_translate = await db.select_last_translate(current_dictionary)
    # print(last_translate)

    # last_dictionary = await db.select_last_dictionary(609200395)
    # print(last_dictionary)

    # learning_translates = await db.select_learning_translates(127)
    # print(learning_translates)

    # import datetime
    # current_datetime = await db.test()
    # current_datetime2 = await db.test2()
    # print(current_datetime.minute)
    # print(current_datetime2)
    # print(current_datetime2 == current_datetime)

    # print(learning_translates[0][2].year)
    # print(datetime.date.today())
    # print(learning_translates[0][2] == datetime.date)

    # await db.set_learning_translate(129, 26)

    # translates = await db.learning_translates(131)
    # translate_values = [x[0] for x in translates]
    # print(random.choice(translate_values))

    # repetition_number = await db.check_repition_number(41)
    # print(repetition_number)

    # translate = await db.translate_info(40)
    # print(translate)

    print("Success!")


loop = asyncio.get_event_loop()
db = loop.run_until_complete(Database.create())
loop.run_until_complete(test())
