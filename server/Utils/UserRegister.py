
from pydantic import BaseModel

class UserRegister(BaseModel):
    username: str
    password: str

class user:
    def __init__(self, user_id, username, password, tokens=0):
        self.user_id = user_id
        self.username = username
        self.password = password
        self.tokens = tokens

class RechargeRequest(BaseModel):
    euro_paid: float

class ChatRequest(BaseModel):
    message: str