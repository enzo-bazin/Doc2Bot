from fastapi import APIRouter, HTTPException, Request
from server.Database.repositories.user_repo import get_user_by_id, update_user_tokens
from server.Utils.UserRegister import RechargeRequest

router = APIRouter()

@router.post("/auth/recharge")
async def recharge_tokens(request: Request, payload: RechargeRequest):
    user_id = getattr(request.state, "user_id", None)
    if not user_id:
        raise HTTPException(status_code=401, detail="Non authentifié")

    # --- PLACE POUR L'IMPLÉMENTATION DU PAIEMENT ---
    # Ici, vous devriez appeler l'API de Stripe, PayPal, etc.
    # Pour l'instant, on simule que le paiement est réussi.
    
    # Arbitrairement : 1€ = 1000 tokens
    tokens_to_add = int(payload.euro_paid * 1000)
    
    user = await get_user_by_id(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="Utilisateur non trouvé")
    
    new_total = user.tokens + tokens_to_add
    await update_user_tokens(user_id, new_total)
    
    return {
        "detail": f"Recharge réussie de {tokens_to_add} tokens.",
        "new_balance": new_total
    }
