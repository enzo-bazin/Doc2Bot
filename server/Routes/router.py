from fastapi import APIRouter
from server.Routes.ping.ping import router as ping_router

router = APIRouter()
router.include_router(ping_router)