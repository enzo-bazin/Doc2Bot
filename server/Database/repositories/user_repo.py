from server.Database.db import get_connexion
from uuid import uuid4
from server.Core.security import hash_password

class user:
    def __init__(self, user_id, username, password, file_ref=None):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.file_ref = file_ref

def add_user(username, password):
    hashed_password = hash_password(password)
    with get_connexion() as conn:
         conn.execute("""
                      INSERT INTO users (
                      user_id, 
                      username, 
                      password,
                      file_ref) 
                      VALUES (?, ?, ?, ?)""", (str(uuid4()), username, hashed_password, None))

def remove_user(username):
    with get_connexion() as conn:
         conn.execute("""
                      DELETE FROM users 
                      WHERE username = ?""", (username,))

def get_user(username):
    with get_connexion() as conn:
         cursor = conn.execute("""
                               SELECT user_id, username, password, file_ref 
                               FROM users 
                               WHERE username = ?""", (username,))
         row = cursor.fetchone()
         if row:
             return user(row[0], row[1], row[2], row[3])
         return None

def update_file_ref(username, file_ref):
    with get_connexion() as conn:
         conn.execute("""
                      UPDATE users 
                      SET file_ref = ? 
                      WHERE username = ?""", (file_ref, username))