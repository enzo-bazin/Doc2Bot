from server.Database.database import get_connexion_to_session_db
from server.Database.temporary_file.store_temp_file import remove_file

async def remove_session_and_files(user_id):
    remove_file(user_id) # Assumed synchronous for now, should check if it needs to be async
    await remove_session(user_id)

async def add_session(user_id, last_seen, status):
    async with get_connexion_to_session_db() as db:
         await db.execute("""
                      INSERT INTO sessions (
                      user_id,
                      last_seen,
                       status)
                      VALUES (?, ?, ?)
                      """, (user_id, last_seen, status))

async def remove_session(user_id):
    async with get_connexion_to_session_db() as db:
         await db.execute("""
                      DELETE FROM sessions 
                      WHERE user_id = ?""", (user_id,))

async def get_session(user_id):
    async with get_connexion_to_session_db() as db:
        async with db.execute("""
                     SELECT * FROM sessions
                     WHERE user_id = ?""", (user_id,)) as cursor:
            return await cursor.fetchone()

async def get_all_sessions():
    async with get_connexion_to_session_db() as db:
        async with db.execute("""
                     SELECT * FROM sessions""") as cursor:
            return await cursor.fetchall()

async def update_last_seen(user_id, last_seen):
    async with get_connexion_to_session_db() as db:
         await db.execute("""
                      UPDATE sessions 
                      SET last_seen = ? 
                      WHERE user_id = ?""", (last_seen, user_id))

async def update_status(user_id, status):
    async with get_connexion_to_session_db() as db:
         await db.execute("""
                      UPDATE sessions 
                      SET status = ? 
                      WHERE user_id = ?""", (status, user_id))
