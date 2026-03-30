# Header: session_connexion.py
from fastapi import APIRouter, BackgroundTasks, Request, HTTPException, UploadFile
from server.Utils.UserRegister import user
from datetime import datetime, timezone
from server.Database.repositories.session_repo import add_session
from server.Database.temporary_file.store_temp_file import store_file

router = APIRouter()

# Create session
@router.post("/session/create")
async def create_session(requests: Request, background_tasks: BackgroundTasks, file: UploadFile):
    user_id = requests.state.user_id
    last_seen = datetime.now(timezone.utc)
    try:
        add_session(user_id, last_seen, "processing")
    except:
        raise HTTPException(status_code=500, detail="Internal Server Error")
    # Add background task to update session status after processing is done
    background_tasks.add_task(store_file, user_id, file)
    #background_tasks.add_task(load_client_pdf, user_id)
    return {"detail": "processing your session..."}
    
