# Header: sessions_disconnect.py
# Header: session_connexion.py
from fastapi import APIRouter, BackgroundTasks, Request, HTTPException, UploadFile
from server.Utils.UserRegister import user
from datetime import datetime, timezone
from server.Database.repositories.session_repo import add_session, remove_session_and_files

router = APIRouter()

# Disconnect session
@router.post("/session/disconnect")
async def disconnect_session(requests: Request, background_tasks: BackgroundTasks, file: UploadFile):
    user_id = requests.state.user_id
    last_seen = datetime.now(timezone.utc)
    try:
        add_session(user_id, last_seen, "disconnected")
    except:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    # Add background task to update session status after processing is done
    background_tasks.add_task(remove_session_and_files, user_id)
    #background_tasks.add_task(load_client_pdf, user_id)
    return {"detail": "disconnected from your session..."}
    
