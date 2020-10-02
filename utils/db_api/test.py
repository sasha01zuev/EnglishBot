import asyncio

from utils.db_api.postgresql import Database


async def test():
    # await db.add_translate(2, 'english_word', 'russian_word')

    # select_dict_for_start = await db.select_dictionary_for_start(609200395)
    # print(select_dict_for_start)

    # select_dictionaries = await db.select_dictionaries(609200395)
    # print(select_dictionaries)
    # print(select_dictionaries[0][1])
    # print([[name[0], name[1]] for name in select_dictionaries])

    # current_dictionary = await db.select_current_dictionary(609200395)
    # translate = await db.select_translate(current_dictionary, word='fak')
    # print(translate)
    print("Success!")


loop = asyncio.get_event_loop()
db = loop.run_until_complete(Database.create())
loop.run_until_complete(test())
