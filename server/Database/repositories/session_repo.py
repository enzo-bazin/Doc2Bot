from server.Database.database import get_connexion_to_session_db
from server.Database.temporary_file.store_temp_file import remove_file

def remove_session_and_files(user_id):
    remove_file(user_id)
    remove_session(user_id)

def add_session(user_id, last_seen, status):
    with get_connexion_to_session_db() as conn:
         conn.execute("""
                      INSERT INTO sessions (
                      user_id,
                      last_seen,
                       status)
                      VALUES (?, ?, ?)
                      """, (user_id, last_seen, status))

def remove_session(user_id):
    with get_connexion_to_session_db() as conn:
         conn.execute("""
                      DELETE FROM sessions 
                      WHERE user_id = ?""", (user_id,))

def get_session(user_id):
    with get_connexion_to_session_db() as conn:
        cursor = conn.execute("""
                     SELECT * FROM sessions
                     WHERE user_id = ?""", (user_id,))
        return cursor.fetchone()

def get_all_sessions():
    with get_connexion_to_session_db() as conn:
        cursor = conn.execute("""
                     SELECT * FROM sessions""")
        return cursor.fetchall()

def update_last_seen(user_id, last_seen):
    with get_connexion_to_session_db() as conn:
         conn.execute("""
                      UPDATE sessions 
                      SET last_seen = ? 
                      WHERE user_id = ?""", (last_seen, user_id))

def update_status(user_id, status):
    with get_connexion_to_session_db() as conn:
         conn.execute("""
                      UPDATE sessions 
                      SET status = ? 
                      WHERE user_id = ?""", (status, user_id))