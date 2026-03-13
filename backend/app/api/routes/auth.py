"""
Rotas de Autenticação
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.services.auth_service import authenticate_user, create_access_token

router = APIRouter()


@router.post("/login")
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_db)
):
    """
    Endpoint de login - retorna token JWT

    Para MVP do TCC, autenticação simplificada.
    Em produção, implementar auth completo.
    """
    # MVP: autenticação simplificada
    # TODO: Implementar autenticação real com banco de dados
    if form_data.username == "admin" and form_data.password == "admin123":
        access_token = create_access_token(data={"sub": form_data.username})
        return {
            "access_token": access_token,
            "token_type": "bearer",
            "user": {
                "username": form_data.username,
                "name": "Administrador",
                "role": "fisioterapeuta"
            }
        }

    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Credenciais inválidas",
        headers={"WWW-Authenticate": "Bearer"},
    )


@router.get("/me")
async def get_current_user():
    """Retorna dados do usuário logado"""
    # MVP: retorna usuário fixo
    # TODO: Implementar com token real
    return {
        "username": "admin",
        "name": "Administrador",
        "role": "fisioterapeuta"
    }
