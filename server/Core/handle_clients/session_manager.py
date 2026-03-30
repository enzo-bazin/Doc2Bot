# Header: session_manager.py
from server.Database.repositories.session_repo import get_all_sessions, remove_session_and_files
from datetime import datetime, timezone

async def cleanup_sessions():
    sessions = get_all_sessions()
    for session in sessions:
        user_id, last_seen, status = session
        if status == "disconnected":
            remove_session_and_files(user_id)
        if (datetime.now(timezone.utc) - datetime.fromisoformat(last_seen)).total_seconds() > 10:
            remove_session_and_files(user_id)