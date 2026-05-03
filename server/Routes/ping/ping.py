from fastapi import APIRouter, Request, HTTPException
from datetime import datetime, timezone
from server.Database.repositories.session_repo import get_session, update_status, update_last_seen

router = APIRouter()

@router.post("/ping")
async def ping(request: Request):
    user_id = getattr(request.state, "user_id", None)
    if not user_id:
        raise HTTPException(status_code=401, detail="User not authenticated")

    time_now = datetime.now(timezone.utc)
    session = await get_session(user_id)
    
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found or expired")
    
    last_seen_str = session[1]
    last_ping = datetime.fromisoformat(last_seen_str)
    
    # Si plus de 30 secondes d'inactivité
    if (time_now - last_ping).total_seconds() > 30:
        await update_status(user_id, "disconnected")
        raise HTTPException(status_code=408, detail="Session timed out")
    
    await update_last_seen(user_id, time_now.isoformat())
    return {"status": "ok"}
