
from pydantic import BaseModel

class UserRegister(BaseModel):
    username: str
    password: str

class user:
    def __init__(self, user_id, username, password, file_ref=None):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.file_ref = file_ref