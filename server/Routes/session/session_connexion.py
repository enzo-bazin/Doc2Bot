# Header: session_connexion.py
from fastapi import APIRouter, BackgroundTasks, HTTPException, UploadFile
from datetime import datetime, timezone
from server.Database.repositories.session_repo import add_session
from server.Database.temporary_file.store_temp_file import store_file

ANONYMOUS_USER_ID = "anonymous"

router = APIRouter()

# Create session
@router.post("/session/create")
async def create_session(background_tasks: BackgroundTasks, file: UploadFile):
    last_seen = datetime.now(timezone.utc).isoformat()
    try:
        await add_session(ANONYMOUS_USER_ID, last_seen, "processing")
    except Exception as e:
        print(f"Error creating session: {e}")
        raise HTTPException(status_code=500, detail="Internal Server Error")

    # Add background task to update session status after processing is done
    background_tasks.add_task(store_file, ANONYMOUS_USER_ID, file)
    return {"detail": "processing your session..."}
