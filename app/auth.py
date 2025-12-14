from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from dotenv import load_dotenv
import os
from passlib.context import CryptContext
from jose import jwt
from datetime import datetime, timedelta
from fastapi.security import HTTPBearer
from fastapi import Depends

load_dotenv()

router = APIRouter()

security = HTTPBearer()

ADMIN_EMAIL = os.getenv("ADMIN_EMAIL")
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD") 
JWT_SECRET = os.getenv("JWT_SECRET")
JWT_ALGORITHM = os.getenv("JWT_ALGORITHM")

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class LoginRequest(BaseModel):
    email: str
    password: str


@router.post("/admin/login")
def admin_login(data: LoginRequest):
    if data.email != ADMIN_EMAIL:
        raise HTTPException(status_code=401,detail="Invalid credentials")

    if data.password != ADMIN_PASSWORD:
        raise HTTPException(status_code=401,detail="Invalid credentials")

    token = jwt.encode(
        {"email": data.email, "exp": datetime.utcnow() + timedelta(hours=10)},
        JWT_SECRET,
        algorithm=JWT_ALGORITHM,
    )

    return {"access_token": token, "token_type": "bearer"}

@router.get("/admin/auth-test", dependencies=[Depends(security)])
def auth_test():
    return {"message": "Token OK"}
