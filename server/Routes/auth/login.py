# Header: login.py
from fastapi import APIRouter, HTTPException
from server.Database.repositories.user_repo import get_user
from server.Utils.UserRegister import UserRegister
from server.Core.security.hashage import verify_password
from jose import jwt
from dotenv import load_dotenv
import os

load_dotenv()
router = APIRouter()

@router.post("/auth/login")
def login(client: UserRegister):
    user = get_user(client.username)
    if not user or not verify_password(client.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    token = jwt.encode({"user_id": user.user_id}, os.getenv("TOKEN_KEY"), algorithm="HS256")
    return {"token": token}
