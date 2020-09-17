from environs import Env

env = Env()
env.read_env()

BOT_TOKEN = env("BOT_TOKEN")
ADMINS_ID = env.list("ADMINS_ID")
print(ADMINS_ID)
