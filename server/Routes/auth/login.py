# Header: login.py
from fastapi import APIRouter, HTTPException
from server.Database.repositories.user_repo import get_user
from server.Utils.UserRegister import UserRegister
from server.Core.security.hashage import verify_password
from jose import jwt
from server.Utils.constants import settings

router = APIRouter()

@router.post("/auth/login")
async def login(client: UserRegister):
    user = await get_user(client.username)
    if not user or not verify_password(client.password, user.password):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    token = jwt.encode(
        {"user_id": user.user_id}, 
        settings.TOKEN_KEY, 
        algorithm=settings.ALGORITHM
    )
    return {"token": token}
