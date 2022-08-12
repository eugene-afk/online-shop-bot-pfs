import os
from envparse import Env

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

env = Env()
env_file_path = os.path.join(BASE_DIR, '.env')
env.read_envfile(env_file_path)

TELEGRAM_API_TOKEN = env.str('TELEGRAM_API_TOKEN', default="12345:qwerty")
TELEGRAM_PAYMENTS_PROVIDER_TOKEN = env.str('TELEGRAM_PAYMENTS_PROVIDER_TOKEN', default="12345:TEST:qwerty")
TELEGRAM_WEB_APP_URL = env.str('TELEGRAM_WEB_APP_URL', default="https://google.com") # without trailing slash
TELEGRAM_ADMINS = env.str('TELEGRAM_ADMINS', default="000,") # separated by comma (,), trailing comma (,) is necessary

DB_HOST = env.str('DB_HOST', default='localhost:3306')
DB_NAME = env.str('DB_NAME', default='osb')
DB_USER = env.str('DB_USER', default='osb')
DB_PASSWORD = env.str('DB_PASSWORD', default='7f3MMfS2n3')
# TEST_DB_NAME = env.str('TEST_DB_NAME', default='osbtest')
# TEST_DB_USER = env.str('TEST_DB_USER', default='osbtest')
# TEST_DB_PASSWORD = env.str('TEST_DB_PASSWORD', default='9pQVKH49#H0w')
DB_MAX_CONNECTIONS = env.int('DB_MAX_CONNECTIONS', default=10)
DC_POOL_RECYCLE = env.int('DC_POOL_RECYCLE', default=60)