from fastapi import APIRouter, BackgroundTasks, Request, HTTPException, UploadFile
from server.Utils.UserRegister import user
from datetime import datetime, timezone
from server.Database.repositories.session_repo import get_session, update_status, update_last_seen

router = APIRouter()

@router.post("/ping")
async def ping(requests: Request, background_tasks: BackgroundTasks, file: UploadFile):
    user_id = requests.state.user_id
    time_now = datetime.now(timezone.utc)
    session = get_session(user_id)
    if session is None:
        raise HTTPException(status_code=404, detail="Session not found or expired")
    last_ping = datetime.fromisoformat(session[1])
    if (time_now - last_ping).total_seconds() > 30:
        update_status(user_id, "disconnected")
        raise HTTPException(status_code=408, detail="Session timed out")
    update_last_seen(user_id, time_now)
    return {"status": "ok"}
