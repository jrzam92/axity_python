from datetime import timedelta
from fastapi import APIRouter, HTTPException, status

from ..schemas.auth import LoginRequest, Token
from ..services.auth_service import authenticate_user, create_access_token
from ..config import settings

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/login", response_model=Token)
def login(credentials: LoginRequest):
    """
    Endpoint de login con JWT
    
    Credenciales de prueba:
    - username: admin
    - password: admin123
    """
    user = authenticate_user(credentials.username, credentials.password)
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Usuario o contraseña incorrectos",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=access_token_expires
    )
    
    return {"access_token": access_token, "token_type": "bearer"}