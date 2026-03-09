# Header: register.py
from fastapi import APIRouter
from pydantic import BaseModel
from server.Database.repositories.user_repo import add_user
from sqlite3 import IntegrityError
from fastapi import HTTPException

class UserRegister(BaseModel):
    username: str
    password: str

router = APIRouter()

@router.post("/auth/register")
def register(user: UserRegister):
    try:
        add_user(user.username, user.password)
        return {"detail": "user registered successfully"}
    except IntegrityError:
        raise HTTPException(status_code=400, detail="Username already exists")
    except Exception as e:
        raise HTTPException(status_code=500, detail="Error occurred while registering user") 