from server.Database.database import get_connexion_to_user_db
from uuid import uuid4
from server.Core.security.hashage import hash_password
from server.Utils.UserRegister import user


def add_user(username, password):
    hashed_password = hash_password(password)
    with get_connexion_to_user_db() as conn:
         conn.execute("""
                      INSERT INTO users (
                      user_id, 
                      username, 
                      password) 
                      VALUES (?, ?, ?)""", (str(uuid4()), username, hashed_password))

def remove_user(username):
    with get_connexion_to_user_db() as conn:
         conn.execute("""
                      DELETE FROM users 
                      WHERE username = ?""", (username,))

def get_user(username):
    with get_connexion_to_user_db() as conn:
         cursor = conn.execute("""
                               SELECT user_id, username, password 
                               FROM users 
                               WHERE username = ?""", (username,))
         row = cursor.fetchone()
         if row:
             return user(row[0], row[1], row[2])
         return None