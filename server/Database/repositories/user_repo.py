from server.Database.database import get_connexion_to_user_db
from uuid import uuid4
from server.Core.security.hashage import hash_password
from server.Utils.UserRegister import user


async def add_user(username, password):
    hashed_password = hash_password(password)
    async with get_connexion_to_user_db() as db:
         await db.execute("""
                      INSERT INTO users (
                      user_id, 
                      username, 
                      password) 
                      VALUES (?, ?, ?)""", (str(uuid4()), username, hashed_password))

async def remove_user(username):
    async with get_connexion_to_user_db() as db:
         await db.execute("""
                      DELETE FROM users 
                      WHERE username = ?""", (username,))

async def get_user(username):
    async with get_connexion_to_user_db() as db:
         async with db.execute("""
                               SELECT user_id, username, password, tokens 
                               FROM users 
                               WHERE username = ?""", (username,)) as cursor:
             row = await cursor.fetchone()
             if row:
                 return user(row[0], row[1], row[2], row[3])
             return None

async def get_user_by_id(user_id):
    async with get_connexion_to_user_db() as db:
         async with db.execute("""
                               SELECT user_id, username, password, tokens 
                               FROM users 
                               WHERE user_id = ?""", (user_id,)) as cursor:
             row = await cursor.fetchone()
             if row:
                 return user(row[0], row[1], row[2], row[3])
             return None

async def update_user_tokens(user_id, new_token_count):
    async with get_connexion_to_user_db() as db:
         await db.execute("""
                      UPDATE users 
                      SET tokens = ? 
                      WHERE user_id = ?""", (new_token_count, user_id))
