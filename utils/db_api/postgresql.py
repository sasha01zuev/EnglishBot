import asyncio

import asyncpg

from asyncpg.pool import Pool
from data import config


class Database:
    def __init__(self, pool):
        self.pool: Pool = pool

    @classmethod
    async def create(cls):
        pool = await asyncpg.create_pool(
            user=config.PGUSER,
            password=config.PGPASSWORD,
            host=config.IP,
            database="english_tg_bot"

        )
        return cls(pool)

    @staticmethod
    def format_args(sql, parameters: dict):
        sql += " AND ".join([
            f"{item} = ${num + 1}" for num, item in enumerate(parameters)
        ])
        return sql, tuple(parameters.values())

    async def add_user(self, tg_id: int, name: str, full_name: str, registration_date, last_action):
        sql = """
           INSERT INTO users(tg_id, name, full_name, registration_date, last_action) 
           VALUES($1, $2, $3, $4, $5);
           """
        await self.pool.execute(sql, tg_id, name, full_name, registration_date, last_action)

    async def add_dictionary(self, user_id: int, name: str):
        sql = """
        INSERT INTO dictionaries(user_id, name) VALUES ($1, $2);
        """
        await self.pool.execute(sql, user_id, name)

    async def select_dictionaries(self, user_id):
        sql = """
        SELECT * FROM dictionaries WHERE user_id = $1;
        """
        return await self.pool.fetch(sql, user_id)

    async def set_current_dictionary(self, user_id, dictionary_id):
        try:
            sql = """
            INSERT INTO current_dictionary(user_id, dictionary_id) VALUES ($1, $2);
            """
            await self.pool.execute(sql, user_id, dictionary_id)
        except asyncpg.exceptions.UniqueViolationError:
            sql = """
            UPDATE current_dictionary SET dictionary_id = $2 WHERE user_id = $1;
            """
            await self.pool.execute(sql, user_id, dictionary_id)

    async def select_last_10_translates(self, dictionary_id):
        sql = """
        SELECT * FROM words WHERE dictionary_id = $1 LIMIT 10;
        """
        return await self.pool.fetch(sql, dictionary_id)

    async def select_dictionary_for_start(self, user_id):
        sql = """
        SELECT id FROM dictionaries WHERE user_id = $1;
        """
        return await self.pool.fetchval(sql, user_id)

    async def select_current_dictionary(self, user_id):
        sql = """
        SELECT dictionary_id FROM current_dictionary WHERE user_id = $1;
        """
        return await self.pool.fetchval(sql, user_id)

    async def add_translate(self, dictionary_id, english, russian):
        sql = """
        INSERT INTO words(dictionary_id, english, russian) VALUES ($1, $2, $3);
        """
        await self.pool.execute(sql, dictionary_id, english, russian)

    async def select_translate(self, dictionary_id, word):
        sql = """
        SELECT * FROM words WHERE ((dictionary_id = $1) 
        AND (lower(english) = LOWER($2) OR lower(russian) = LOWER($2)));
        """
        return await self.pool.fetch(sql, dictionary_id, word)

    async def select_last_translate(self, dictionary_id):
        sql = """
        SELECT * FROM words WHERE dictionary_id = $1 ORDER BY id DESC LIMIT 1;
        """
        return await self.pool.fetchrow(sql, dictionary_id)

    async def delete_translate(self, dictionary_id, word):
        sql = """
        DELETE  FROM words WHERE ((dictionary_id = $1) AND (english = $2 OR russian = $2));
        """
        await self.pool.execute(sql, dictionary_id, word)

    async def delete_translate_accurate(self, dictionary_id, english_word, russian_word):
        sql = """
        DELETE  FROM words WHERE ((dictionary_id = $1) AND (english = $2 AND russian = $3));
        """
        await self.pool.execute(sql, dictionary_id, english_word, russian_word)

    async def select_last_dictionary(self, tg_id):
        sql = """
        SELECT * FROM dictionaries WHERE user_id = $1 ORDER BY id DESC LIMIT 1;
        """
        return await self.pool.fetchrow(sql, tg_id)

    async def delete_dictionary(self, dictionary_id):
        sql = """
        DELETE FROM dictionaries WHERE id = $1;
        """
        await self.pool.execute(sql, dictionary_id)

    async def select_dictionary(self, dictionary_id):
        sql = """
        SELECT * FROM  dictionaries WHERE id = $1;
        """
        return await self.pool.fetchrow(sql, dictionary_id)
