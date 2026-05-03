# Header: middleware.py
from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request
from jose import jwt, JWTError
from starlette.responses import JSONResponse
from server.Utils.constants import settings

PUBLIC_ROUTES = ["/auth/register", "/auth/login"]

class AuthentificationMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        # Allow public routes
        if any(request.url.path.startswith(route) for route in PUBLIC_ROUTES):
            return await call_next(request)

        bearer_token = request.headers.get("authorization")
        if not bearer_token or not bearer_token.startswith("Bearer "):
            return JSONResponse(
                status_code=401, 
                content={"detail": "Missing or invalid token"}
            )

        token = bearer_token.split(" ")[1]
        try:
            decoded_token = jwt.decode(
                token, 
                key=settings.TOKEN_KEY, 
                algorithms=[settings.ALGORITHM]
            )
            user_id = decoded_token.get("user_id")
            if not user_id:
                raise JWTError("user_id not in token")
            request.state.user_id = user_id
        except JWTError:
            return JSONResponse(
                status_code=401, 
                content={"detail": "Invalid or expired token"}
            )
        except Exception as e:
            print(f"Middleware Error: {e}")
            return JSONResponse(
                status_code=500, 
                content={"detail": "Internal Server Error"}
            )

        response = await call_next(request)
        return response
