from fastapi import APIRouter
from server.Routes.ping.ping import router as ping_router
from server.Routes.auth.register import router as register_router
from server.Routes.auth.login import router as login_router
from server.Routes.auth.recharge import router as recharge_router
from server.Routes.session.session_connexion import router as session_router
from server.Routes.chabot.chatbot import router as chatbot_router

router = APIRouter()
router.include_router(ping_router)
router.include_router(register_router)
router.include_router(login_router)
router.include_router(recharge_router)
router.include_router(session_router)
router.include_router(chatbot_router)
