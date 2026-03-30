# Header: mainloop.py

import sys
import asyncio
from pathlib import Path

from fastapi.concurrency import asynccontextmanager

# Add project root to sys.path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from fastapi import FastAPI
from server.Routes.router import router as main_router
import uvicorn
from server.Database.database import init_db
from server.Core.handle_event.middleware import AuthentificationMiddleware
from server.Core.handle_clients.session_manager import cleanup_sessions

init_db()

async def main_loop():
    while True:
        await cleanup_sessions()
        await asyncio.sleep(10)

@asynccontextmanager
async def lifespan(app: FastAPI):
    task = asyncio.create_task(main_loop())
    yield
    task.cancel()


app = FastAPI(lifespan=lifespan)
app.add_middleware(AuthentificationMiddleware)
app.include_router(main_router)


# Start the server
uvicorn.run(app, host="0.0.0.0", port=8000)