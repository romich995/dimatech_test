from sqlalchemy import create_engine, insert
import os

from utils import hash_password
from models import Base, User, Administrator, Account

DB_CONN = (f'postgresql://'
           f'{os.environ.get("POSTGRES_USER")}:'
           f'{os.environ.get("POSTGRES_PASSWORD")}@'
           f'{os.environ.get("POSTGRES_HOST")}:'
           f'{os.environ.get("POSTGRES_PORT")}/'
           f'{os.environ.get("POSTGRES_DB")}')

engine = create_engine(DB_CONN)
Base.metadata.create_all(engine)

with engine.connect() as conn:
    stmt = insert(User).values(full_name="test",
                               email="test@test.test",
                               hashed_password=hash_password('test')
                               )
    conn.execute(stmt)
    stmt = insert(Administrator).values(full_name="admin",
                               email="admin@test.test",
                               hashed_password=hash_password('admin')
                               )
    conn.execute(stmt)

    stmt = insert(Account).values(user_id=1,
                                  balance=0,
                                        )
    conn.execute(stmt)


