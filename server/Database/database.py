import aiosqlite
from server.Utils.constants import settings
from contextlib import asynccontextmanager

@asynccontextmanager
async def get_connexion_to_user_db():
    async with aiosqlite.connect(settings.USER_DB_PATH) as db:
        yield db
        await db.commit()

@asynccontextmanager
async def get_connexion_to_session_db():
    async with aiosqlite.connect(settings.SESSION_DB_PATH) as db:
        yield db
        await db.commit()

async def init_db():
    async with get_connexion_to_user_db() as db:
        await db.execute("""
                     CREATE TABLE IF NOT EXISTS users (
                     user_id TEXT PRIMARY KEY,
                     username TEXT UNIQUE NOT NULL,
                     password TEXT NOT NULL,
                     tokens INTEGER DEFAULT 0)"""
                     )
    async with get_connexion_to_session_db() as db:
        await db.execute("""
                     CREATE TABLE IF NOT EXISTS sessions (
                     user_id TEXT PRIMARY KEY,
                     last_seen TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                     status TEXT NOT NULL)
                     """)
