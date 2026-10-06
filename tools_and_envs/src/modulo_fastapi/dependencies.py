from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session

from .database import get_db
from .services.auth_service import decode_token

security = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security)
) -> str:
    """
    Dependencia que valida JWT en header Authorization
    Retorna username del usuario autenticado
    """
    token = credentials.credentials
    token_data = decode_token(token)
    return token_data.username

# Alias para mayor claridad
CurrentUser = Depends(get_current_user)
DatabaseSession = Depends(get_db)