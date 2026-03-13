"""
Rotas de Pacientes - CRUD
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.database import get_db
from app.db import crud
from app.schemas.paciente import PacienteCreate, PacienteUpdate, PacienteResponse

router = APIRouter()


@router.get("/", response_model=List[PacienteResponse])
async def listar_pacientes(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db)
):
    """Lista todos os pacientes"""
    pacientes = await crud.get_pacientes(db, skip=skip, limit=limit)
    return pacientes


@router.get("/{paciente_id}", response_model=PacienteResponse)
async def obter_paciente(
    paciente_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Obtém um paciente pelo ID"""
    paciente = await crud.get_paciente(db, paciente_id)
    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paciente não encontrado"
        )
    return paciente


@router.post("/", response_model=PacienteResponse, status_code=status.HTTP_201_CREATED)
async def criar_paciente(
    paciente: PacienteCreate,
    db: AsyncSession = Depends(get_db)
):
    """Cria um novo paciente"""
    return await crud.create_paciente(db, paciente)


@router.put("/{paciente_id}", response_model=PacienteResponse)
async def atualizar_paciente(
    paciente_id: int,
    paciente: PacienteUpdate,
    db: AsyncSession = Depends(get_db)
):
    """Atualiza um paciente existente"""
    db_paciente = await crud.update_paciente(db, paciente_id, paciente)
    if not db_paciente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paciente não encontrado"
        )
    return db_paciente


@router.delete("/{paciente_id}", status_code=status.HTTP_204_NO_CONTENT)
async def deletar_paciente(
    paciente_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Deleta um paciente"""
    success = await crud.delete_paciente(db, paciente_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paciente não encontrado"
        )
