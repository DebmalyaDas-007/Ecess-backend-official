from starlette.middleware.base import BaseHTTPMiddleware
from fastapi import Request, HTTPException
from jose import jwt
import os

JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")
ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")

class AdminAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):

        path = request.url.path

        if path.startswith("/admin") and path != "/admin/login":

            auth_header = request.headers.get("Authorization")
            if not auth_header or not auth_header.startswith("Bearer "):
                raise HTTPException(status_code=401, detail="Missing or invalid token")

            token = auth_header.split(" ")[1]

            try:
                payload = jwt.decode(token, JWT_SECRET, algorithms=[JWT_ALGORITHM])
            except Exception:
                raise HTTPException(status_code=401, detail="Invalid or expired token")

            if payload.get("email") != ADMIN_EMAIL:
                raise HTTPException(status_code=403, detail="Not authorized as admin")

        response = await call_next(request)
        return response
