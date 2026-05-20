from fastapi import APIRouter
from server.Routes.ping.ping import router as ping_router
from server.Routes.session.session_connexion import router as session_router
from server.Routes.chabot.chatbot import router as chatbot_router

router = APIRouter()
router.include_router(ping_router)
router.include_router(session_router)
router.include_router(chatbot_router)
