from fastapi import APIRouter
from server.Routes.ping.ping import router as ping_router
from server.Routes.auth.register import router as register_router
from server.Routes.auth.login import router as login_router

router = APIRouter()
router.include_router(ping_router)
router.include_router(register_router)
router.include_router(login_router)