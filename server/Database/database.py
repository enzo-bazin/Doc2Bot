import sqlite3
from contextlib import contextmanager

@contextmanager
def get_connexion_to_user_db(path='server/Database/db/users.db'):
    connexion = sqlite3.connect(path)
    try:
        yield connexion
        connexion.commit()
    finally:
        connexion.close()

@contextmanager
def get_connexion_to_session_db(path='server/Database/db/session.db'):
    connexion = sqlite3.connect(path)
    try:
        yield connexion
        connexion.commit()
    finally:
        connexion.close()

def init_db():
    with get_connexion_to_user_db() as conn:
        conn.execute("""
                     CREATE TABLE IF NOT EXISTS users (
                     user_id TEXT PRIMARY KEY,
                     username TEXT UNIQUE NOT NULL,
                     password TEXT NOT NULL)"""
                     )
    with get_connexion_to_session_db() as conn:
        conn.execute("""
                     CREATE TABLE IF NOT EXISTS sessions (
                     user_id TEXT PRIMARY KEY,
                     last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP)
                     """)