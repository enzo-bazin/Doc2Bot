import sqlite3
from contextlib import contextmanager

@contextmanager
def get_connexion(path='Database/db/users.db'):
    connexion = sqlite3.connect(path)
    try:
        yield connexion
        connexion.commit()
    finally:
        connexion.close()

def init_db():
    with get_connexion() as conn:
        conn.execute("""
                     CREATE TABLE IF NOT EXISTS users (
                     user_id TEXT PRIMARY KEY,
                     username TEXT UNIQUE NOT NULL,
                     password TEXT NOT NULL,
                     file_ref TEXT)"""
                     )