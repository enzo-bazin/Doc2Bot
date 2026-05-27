from fastapi import APIRouter, HTTPException, Request
from server.Database.repositories.user_repo import get_user_by_id, update_user_tokens
from server.Utils.UserRegister import ChatRequest

router = APIRouter()

@router.post("/chatbot/chat")
async def chat(request: Request, payload: ChatRequest):
    user_id = getattr(request.state, "user_id", None)
    if not user_id:
        raise HTTPException(status_code=401, detail="Non authentifié")
    
    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    if user.tokens <= 0:
        raise HTTPException(status_code=403, detail="Crédits insuffisants. Veuillez recharger.")

 # --- PLACE POUR L'APPEL AU LLM (OpenAI, Anthropic, etc.) ---
    # Ici, vous enverriez 'payload.message' au modèle d'IA.
    # On simule une réponse et une consommation de tokens.
    simulated_response = f"Ceci est une réponse simulée à votre message : '{payload.message}'"
    
    tokens_used = len(payload.message.split()) + 10 # Simulation simple
    
    if user.tokens < tokens_used:
         raise HTTPException(status_code=403, detail="Pas assez de tokens pour cette requête.")

    # Mise à jour des tokens dans la DB
    new_balance = user.tokens - tokens_used
    await update_user_tokens(user_id, new_balance)
    
    return {
        "response": simulated_response,
        "tokens_used": tokens_used,
        "remaining_tokens": new_balance
    }