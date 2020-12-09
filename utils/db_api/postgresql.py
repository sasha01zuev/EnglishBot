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

    async def add_user(self, tg_id: int, name: str, full_name: str, username: str):
        sql = """
           INSERT INTO users(tg_id, name, full_name, username) 
           VALUES($1, $2, $3, $4);
           """
        await self.pool.execute(sql, tg_id, name, full_name, username)

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
        SELECT * FROM translates WHERE dictionary_id = $1 ORDER BY id DESC LIMIT 10;
        """
        return await self.pool.fetch(sql, dictionary_id)

    async def select_dictionary_id_for_start(self, user_id):
        sql = """
        SELECT id FROM dictionaries WHERE user_id = $1;
        """
        return await self.pool.fetchval(sql, user_id)

    async def select_current_dictionary(self, user_id):
        sql = """
        SELECT dictionary_id FROM current_dictionary WHERE user_id = $1;
        """
        return await self.pool.fetchval(sql, user_id)

    async def add_translate(self, english_word, russian_word, dictionary_id):
        sql = """
        INSERT INTO translates(english_word, russian_word, dictionary_id) VALUES ($1, $2, $3);
        """
        await self.pool.execute(sql, english_word, russian_word, dictionary_id)

    async def select_translate(self, dictionary_id, word):
        sql = """
        SELECT * FROM translates WHERE ((dictionary_id = $1) 
        AND (lower(english_word) = LOWER($2) OR lower(russian_word) = LOWER($2)));
        """
        return await self.pool.fetch(sql, dictionary_id, word)

    async def translate_info(self, translate_id):
        sql = """
        SELECT * FROM translates WHERE id = $1;
        """
        return await self.pool.fetchrow(sql, translate_id)

    async def select_last_translate(self, dictionary_id):
        sql = """
        SELECT * FROM translates WHERE dictionary_id = $1 ORDER BY id DESC LIMIT 1;
        """
        return await self.pool.fetchrow(sql, dictionary_id)

    async def delete_translate(self, dictionary_id, word):
        sql = """
        DELETE  FROM translates WHERE ((dictionary_id = $1) AND (english_word = $2 OR russian_word = $2));
        """
        await self.pool.execute(sql, dictionary_id, word)

    async def delete_translate_accurate(self, dictionary_id, english_word, russian_word):
        sql = """
        DELETE  FROM translates WHERE ((dictionary_id = $1) AND (english_word = $2 AND russian_word = $3));
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

    async def add_message(self, user_id, message):
        sql = """
        INSERT INTO messages(user_id, message, date_time)
        VALUES ($1, $2, NOW());
        """
        await self.pool.execute(sql, user_id, message)

    async def add_last_action(self, user_id):
        sql = """
        UPDATE user_parameters SET last_action = NOW() WHERE user_id = $1;
        """
        await self.pool.execute(sql, user_id)

    async def set_user_parameters(self, user_id, reverse_translate, user_language):
        sql = """
        INSERT INTO user_parameters(user_id, registration_date, last_action, reverse_translate, user_language)
        VALUES ($1,NOW(),NOW(),$2, $3);
        """
        await self.pool.execute(sql, user_id, reverse_translate, user_language)

    async def get_user_language(self, user_id):
        sql = """
        SELECT user_language FROM user_parameters WHERE  user_id = $1;
        """
        return await self.pool.fetchval(sql, user_id)

    # LEARNING PROCCESS REQUESTS

    async def select_learning_translates(self, dictionary_id):
        sql = """
        SELECT * FROM learn_translate WHERE dictionary_id = $1;
        """
        return await self.pool.fetch(sql, dictionary_id)

    async def set_learning_translate(self, dictionary_id, translate_id):
        sql = """
        INSERT INTO learn_translate(dictionary_id, translate_id, approach_date)
        VALUES ($1, $2, NOW());
        """
        await self.pool.execute(sql, dictionary_id, translate_id)

    async def update_translate(self, translate_id, dictionary_id, repetition_number):
        if repetition_number == 0:
            try:
                sql = """
                UPDATE learn_translate SET times_repeat = times_repeat + 1 
                WHERE translate_id = $1 AND dictionary_id = $2;
                """
                await self.pool.execute(sql, translate_id, dictionary_id)
            except:
                sql = """
                INSERT INTO first_repeat(dictionary_id, translate_id, approach_date)
                VALUES ($2, $1, NOW() + interval '30 minute')
                """
                await self.pool.execute(sql, translate_id, dictionary_id)

                sql = """
                DELETE FROM learn_translate WHERE translate_id = $1
                """
                await self.pool.execute(sql, translate_id)
        if repetition_number == 1:
            sql = """
            INSERT INTO second_repeat(dictionary_id, translate_id, approach_date)
            VALUES ($2, $1, NOW() + interval '8 hour')
            """
            await self.pool.execute(sql, translate_id, dictionary_id)

            sql = """
            DELETE FROM first_repeat WHERE translate_id = $1
            """
            await self.pool.execute(sql, translate_id)
        if repetition_number == 2:
            sql = """
            INSERT INTO third_repeat(dictionary_id, translate_id, approach_date)
            VALUES ($2, $1, NOW() + interval '1 day')
            """
            await self.pool.execute(sql, translate_id, dictionary_id)

            sql = """
            DELETE FROM second_repeat WHERE translate_id = $1
            """
            await self.pool.execute(sql, translate_id)
        if repetition_number == 3:
            sql = """
            INSERT INTO fourth_repeat(dictionary_id, translate_id, approach_date)
            VALUES ($2, $1, NOW() + interval '3 day')
            """
            await self.pool.execute(sql, translate_id, dictionary_id)

            sql = """
            DELETE FROM third_repeat WHERE translate_id = $1
            """
            await self.pool.execute(sql, translate_id)
        if repetition_number == 4:
            sql = """
            INSERT INTO fifth_repeat(dictionary_id, translate_id, approach_date)
            VALUES ($2, $1, NOW() + interval '7 day')
            """
            await self.pool.execute(sql, translate_id, dictionary_id)

            sql = """
            DELETE FROM fourth_repeat WHERE translate_id = $1
            """
            await self.pool.execute(sql, translate_id)
        if repetition_number == 5:
            sql = """
            INSERT INTO sixth_repeat(dictionary_id, translate_id, approach_date)
            VALUES ($2, $1, NOW() + interval '14 day')
            """
            await self.pool.execute(sql, translate_id, dictionary_id)

            sql = """
            DELETE FROM fifth_repeat WHERE translate_id = $1
            """
            await self.pool.execute(sql, translate_id)
        if repetition_number == 6:
            sql = """
            INSERT INTO seventh_repeat(dictionary_id, translate_id, approach_date)
            VALUES ($2, $1, NOW() + interval '31 day')
            """
            await self.pool.execute(sql, translate_id, dictionary_id)

            sql = """
            DELETE FROM sixth_repeat WHERE translate_id = $1
            """
            await self.pool.execute(sql, translate_id)
        elif repetition_number == 7:
            sql = """
            INSERT INTO learned_translates(dictionary_id, translate_id)
            VALUES ($2, $1)
            """
            await self.pool.execute(sql, translate_id, dictionary_id)

            sql = """
            DELETE FROM seventh_repeat WHERE translate_id = $1
            """
            await self.pool.execute(sql, translate_id)
        else:
            pass

    async def check_repetition_number(self, translate_id):
        sql = """
        SELECT repetition_number FROM translates WHERE id = $1;
        """
        return await self.pool.fetchval(sql, translate_id)

    async def select_random_learning_translate(self, dictionary_id):
        sql = """
        SELECT * FROM translates
        WHERE id = (SELECT translate_id FROM learn_translate WHERE dictionary_id = $1 ORDER BY random() LIMIT 1);
        """
        return await self.pool.fetchrow(sql, dictionary_id)

    async def set_last_learning_translate(self, user_id, translate_id):
        sql = """
        UPDATE user_parameters SET last_learning_translate = $2 WHERE user_id = $1;
        """
        await self.pool.execute(sql, user_id, translate_id)

    async def select_last_learning_translate(self, user_id):
        sql = """
        SELECT last_learning_translate FROM user_parameters
        WHERE user_id = $1;
        """
        return await self.pool.fetchval(sql, user_id)

    async def current_datetime(self):
        sql = """
        SELECT NOW();
        """
        return await self.pool.fetchval(sql)

    async def learning_translates(self, dictionary_id):
        sql = """
        SELECT translate_id FROM learn_translate WHERE (approach_date < NOW()) AND (dictionary_id = $1)
        UNION
        SELECT translate_id FROM first_repeat WHERE (approach_date < NOW()) AND (dictionary_id = $1)
        UNION
        SELECT translate_id FROM second_repeat WHERE (approach_date < NOW()) AND (dictionary_id = $1) 
        UNION
        SELECT translate_id FROM third_repeat WHERE (approach_date < NOW()) AND (dictionary_id = $1)
        UNION
        SELECT translate_id FROM fourth_repeat WHERE (approach_date < NOW()) AND (dictionary_id = $1)
        UNION
        SELECT translate_id FROM fifth_repeat WHERE (approach_date < NOW()) AND (dictionary_id = $1)
        UNION
        SELECT translate_id FROM sixth_repeat WHERE (approach_date < NOW()) AND (dictionary_id = $1)
        UNION
        SELECT translate_id FROM seventh_repeat WHERE (approach_date < NOW()) AND (dictionary_id = $1)
        """
        return await self.pool.fetch(sql, dictionary_id)
