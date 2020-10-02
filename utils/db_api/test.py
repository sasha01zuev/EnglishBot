import asyncio

from utils.db_api.postgresql import Database


async def test():
    # await db.add_translate(2, 'english_word', 'russian_word')

    select_dict_for_start = await db.select_dictionary_for_start(609200395)
    print(select_dict_for_start)

    print("Success!")


loop = asyncio.get_event_loop()
db = loop.run_until_complete(Database.create())
loop.run_until_complete(test())
