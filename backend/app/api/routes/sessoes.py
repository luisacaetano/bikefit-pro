"""
Rotas de Sessões de Bike Fit
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.database import get_db
from app.db import crud
from app.schemas.sessao import SessaoCreate, SessaoResponse

router = APIRouter()


@router.get("/paciente/{paciente_id}", response_model=List[SessaoResponse])
async def listar_sessoes_paciente(
    paciente_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Lista todas as sessões de um paciente"""
    sessoes = await crud.get_sessoes_by_paciente(db, paciente_id)
    return sessoes


@router.get("/{sessao_id}", response_model=SessaoResponse)
async def obter_sessao(
    sessao_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Obtém uma sessão pelo ID"""
    sessao = await crud.get_sessao(db, sessao_id)
    if not sessao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sessão não encontrada"
        )
    return sessao


@router.post("/", response_model=SessaoResponse, status_code=status.HTTP_201_CREATED)
async def criar_sessao(
    sessao: SessaoCreate,
    db: AsyncSession = Depends(get_db)
):
    """Cria uma nova sessão de bike fit"""
    return await crud.create_sessao(db, sessao)


@router.put("/{sessao_id}/finalizar", response_model=SessaoResponse)
async def finalizar_sessao(
    sessao_id: int,
    angulos_depois: dict,
    ajustes: dict,
    db: AsyncSession = Depends(get_db)
):
    """Finaliza uma sessão com os dados pós-ajuste"""
    sessao = await crud.finalizar_sessao(db, sessao_id, angulos_depois, ajustes)
    if not sessao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sessão não encontrada"
        )
    return sessao
