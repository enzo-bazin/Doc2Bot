from fastapi import APIRouter
from server.Utils.UserRegister import ChatRequest

router = APIRouter()

@router.post("/chatbot/chat")
async def chat(payload: ChatRequest):
    # --- PLACE POUR L'APPEL AU LLM (OpenAI, Anthropic, etc.) ---
    simulated_response = f"Ceci est une réponse simulée à votre message : '{payload.message}'"
    return {"response": simulated_response}
