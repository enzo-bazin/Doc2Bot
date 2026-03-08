# Header: mainloop.py

import sys
from pathlib import Path

# Add project root to sys.path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from fastapi import FastAPI
from server.Routes.router import router as main_router
import uvicorn

app = FastAPI()
app.include_router(main_router)

# Start the server
uvicorn.run(app, host="0.0.0.0", port=8000)