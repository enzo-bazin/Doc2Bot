# Header: middleware.py
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import HTTPException, Request, Header
from jose import jwt
from starlette.responses import JSONResponse
from dotenv import load_dotenv
import os

load_dotenv()
PUBLIC_ROUTES = ["/auth/register", "/auth/login"]

class AuthentificationMiddleware (BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        if request.url.path in PUBLIC_ROUTES:
            return await call_next(request)
        bearer_token = request.headers.get("authorization")
        if not bearer_token or not bearer_token.startswith("Bearer "):
            return JSONResponse(status_code=401, content={"detail": "Missing or invalid token"})
        token = bearer_token.split(" ")[1]
        try:
            decoded_token = jwt.decode(token, key=os.getenv("TOKEN_KEY"))
            request.state.user_id = decoded_token.get("user_id")
        except:
            return JSONResponse(status_code=401, content={"detail": "Missing or invalid token"})
        response = await call_next(request)
        return response
