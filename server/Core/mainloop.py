# Header: mainloop.py

import asyncio
from contextlib import asynccontextmanager

from fastapi import FastAPI
import uvicorn

from server.Routes.router import router as main_router
from server.Database.database import init_db
from server.Core.handle_event.middleware import AuthentificationMiddleware
from server.Core.handle_clients.session_manager import cleanup_sessions
from server.Utils.constants import settings

async def main_loop():
    while True:
        try:
            await cleanup_sessions()
        except Exception as e:
            print(f"Error in cleanup_sessions: {e}")
        await asyncio.sleep(10)

@asynccontextmanager
async def lifespan(app: FastAPI):
    # Initialisation de la DB
    await init_db()
    # Lancement de la tâche de fond
    task = asyncio.create_task(main_loop())
    yield
    task.cancel()
    try:
        await task
    except asyncio.CancelledError:
        pass

app = FastAPI(title="Doc2Bot API", lifespan=lifespan)
app.add_middleware(AuthentificationMiddleware)
app.include_router(main_router)

if __name__ == "__main__":
    # Start the server using settings
    uvicorn.run(
        "server.Core.mainloop:app", 
        host=settings.HOST, 
        port=settings.PORT, 
        reload=True
    )
