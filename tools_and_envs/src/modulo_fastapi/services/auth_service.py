from datetime import datetime, timedelta
from jose import JWTError, jwt
from fastapi import HTTPException, status
import hashlib

from ..config import settings
from ..schemas.auth import TokenData

def hash_password(password: str) -> str:
    """Hash simple SHA256 (SOLO PARA DESARROLLO)"""
    return hashlib.sha256(password.encode()).hexdigest()

def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica contraseña contra hash"""
    return hash_password(plain_password) == hashed_password

# Usuario fake para el laboratorio
FAKE_USERS_DB = {
    "admin": {
        "username": "admin",
        # Hash SHA256 de "admin123"
        "hashed_password": "240be518fabd2724ddb6f04eeb1da5967448d7e831c08c8fa822809f74c720a9",
        "disabled": False,
    }
}

def authenticate_user(username: str, password: str):
    """Autentica usuario"""
    user = FAKE_USERS_DB.get(username)
    if not user:
        return False
    if not verify_password(password, user["hashed_password"]):
        return False
    return user

def create_access_token(data: dict, expires_delta: timedelta | None = None):
    """Crea token JWT"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt

def decode_token(token: str) -> TokenData:
    """Decodifica y valida token JWT"""
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="No se pudo validar las credenciales",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
        return TokenData(username=username)
    except JWTError:
        raise credentials_exception