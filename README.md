Vocabulary learning assistant bot
=================================

* * *

Asynchronous telegram bot technologies:

*   Python 3.8.5
*   Aiogram 2.9.2
*   Async DB PostgreSQL - Asyncpg 0.21.0

* * *

The project was made to help people learn foreign words. This is not just a test for added words! The bot has its own training system partially borrowed from the Ebbinghaus graph

![](/pictures/Learning_system.png)

The main logic is located in the folder with handlers. All DB queries located in utils/db\_api/postgresql.py
