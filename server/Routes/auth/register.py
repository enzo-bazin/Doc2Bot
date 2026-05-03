# Header: register.py
from fastapi import APIRouter, HTTPException
from server.Database.repositories.user_repo import add_user
import sqlite3
from server.Utils.UserRegister import UserRegister

router = APIRouter()

@router.post("/auth/register")
async def register(user: UserRegister):
    try:
        await add_user(user.username, user.password)
        return {"detail": "user registered successfully"}
    except sqlite3.IntegrityError:
        raise HTTPException(status_code=400, detail="Username already exists")
    except Exception as e:
        print(f"Error occurred while registering user: {type(e).__name__}: {e}")
        raise HTTPException(status_code=500, detail="Error occurred while registering user")
