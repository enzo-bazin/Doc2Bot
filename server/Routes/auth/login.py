# Header: login.py
from fastapi import APIRouter

router = APIRouter()

@router.get("/auth/login")
def login():
    return {"status": "command not implemented yet"}
