import os

SALT = 'dsngbdjkfmld;'

DB_CONN = (f'postgresql+asyncpg://'
           f'{os.environ.get("POSTGRES_USER")}:'
           f'{os.environ.get("POSTGRES_PASSWORD")}@'
           f'{os.environ.get("POSTGRES_HOST")}:'
           f'{os.environ.get("POSTGRES_PORT")}/'
           f'{os.environ.get("POSTGRES_DB")}')
