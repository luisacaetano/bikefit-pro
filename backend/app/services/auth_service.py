"""
Serviço de Autenticação
"""
from datetime import datetime, timedelta
from typing import Optional
from jose import JWTError, jwt
from passlib.context import CryptContext
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.config import get_settings

settings = get_settings()

# Configuração do hashing de senha
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# OAuth2 scheme
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verifica se a senha está correta"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """Gera hash da senha"""
    return pwd_context.hash(password)


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Cria token JWT

    Args:
        data: Dados a serem codificados no token
        expires_delta: Tempo de expiração

    Returns:
        Token JWT
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.access_token_expire_minutes)

    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm
    )

    return encoded_jwt


def decode_access_token(token: str) -> Optional[dict]:
    """
    Decodifica token JWT

    Args:
        token: Token JWT

    Returns:
        Dados decodificados ou None se inválido
    """
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm]
        )
        return payload
    except JWTError:
        return None


async def authenticate_user(username: str, password: str) -> Optional[dict]:
    """
    Autentica usuário

    Para MVP do TCC, autenticação simplificada.
    Em produção, deve consultar banco de dados.

    Args:
        username: Nome de usuário
        password: Senha

    Returns:
        Dados do usuário ou None se inválido
    """
    # MVP: credenciais fixas
    # TODO: Implementar com banco de dados
    if username == "admin" and password == "admin123":
        return {
            "username": "admin",
            "name": "Administrador",
            "role": "fisioterapeuta"
        }
    return None


async def get_current_user(token: str = Depends(oauth2_scheme)) -> dict:
    """
    Obtém usuário atual do token

    Args:
        token: Token JWT

    Returns:
        Dados do usuário

    Raises:
        HTTPException: Se token inválido
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )

    payload = decode_access_token(token)
    if payload is None:
        raise credentials_exception

    username: str = payload.get("sub")
    if username is None:
        raise credentials_exception

    # MVP: retorna dados fixos
    # TODO: Buscar no banco de dados
    return {
        "username": username,
        "name": "Administrador",
        "role": "fisioterapeuta"
    }
