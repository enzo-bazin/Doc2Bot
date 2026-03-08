# Header: register.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/auth/register")
def register():
    return {"status": "command not implemented yet"}
