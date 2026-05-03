# Header: sessions_disconnect.py
from fastapi import APIRouter, Request, HTTPException
from datetime import datetime, timezone
from server.Database.repositories.session_repo import update_status, remove_session_and_files

router = APIRouter()

@router.post("/session/disconnect")
async def disconnect_session(request: Request):
    user_id = getattr(request.state, "user_id", None)
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")
        
    try:
        await update_status(user_id, "disconnected")
        # On peut supprimer immédiatement ou laisser le cleanup s'en charger
        await remove_session_and_files(user_id)
        return {"detail": "disconnected successfully"}
    except Exception as e:
        print(f"Error disconnecting: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")
