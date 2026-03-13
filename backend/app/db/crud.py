"""
CRUD operations - Create, Read, Update, Delete
"""
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from sqlalchemy.orm import selectinload
from typing import List, Optional
from datetime import datetime

from app.db.models import Paciente, Sessao, Medida
from app.schemas.paciente import PacienteCreate, PacienteUpdate
from app.schemas.sessao import SessaoCreate


# ============================================
# PACIENTES
# ============================================

async def get_pacientes(db: AsyncSession, skip: int = 0, limit: int = 100) -> List[Paciente]:
    """Lista todos os pacientes"""
    result = await db.execute(
        select(Paciente).offset(skip).limit(limit).order_by(Paciente.nome)
    )
    return result.scalars().all()


async def get_paciente(db: AsyncSession, paciente_id: int) -> Optional[Paciente]:
    """Obtém um paciente pelo ID"""
    result = await db.execute(
        select(Paciente).where(Paciente.id == paciente_id)
    )
    return result.scalar_one_or_none()


async def create_paciente(db: AsyncSession, paciente: PacienteCreate) -> Paciente:
    """Cria um novo paciente"""
    db_paciente = Paciente(**paciente.model_dump())
    db.add(db_paciente)
    await db.commit()
    await db.refresh(db_paciente)
    return db_paciente


async def update_paciente(db: AsyncSession, paciente_id: int, paciente: PacienteUpdate) -> Optional[Paciente]:
    """Atualiza um paciente existente"""
    db_paciente = await get_paciente(db, paciente_id)
    if not db_paciente:
        return None

    update_data = paciente.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(db_paciente, key, value)

    await db.commit()
    await db.refresh(db_paciente)
    return db_paciente


async def delete_paciente(db: AsyncSession, paciente_id: int) -> bool:
    """Deleta um paciente"""
    db_paciente = await get_paciente(db, paciente_id)
    if not db_paciente:
        return False

    await db.delete(db_paciente)
    await db.commit()
    return True


# ============================================
# SESSÕES
# ============================================

async def get_sessoes_by_paciente(db: AsyncSession, paciente_id: int) -> List[Sessao]:
    """Lista todas as sessões de um paciente"""
    result = await db.execute(
        select(Sessao)
        .where(Sessao.paciente_id == paciente_id)
        .order_by(Sessao.data.desc())
    )
    return result.scalars().all()


async def get_sessao(db: AsyncSession, sessao_id: int) -> Optional[Sessao]:
    """Obtém uma sessão pelo ID"""
    result = await db.execute(
        select(Sessao).where(Sessao.id == sessao_id)
    )
    return result.scalar_one_or_none()


async def create_sessao(db: AsyncSession, sessao: SessaoCreate) -> Sessao:
    """Cria uma nova sessão"""
    db_sessao = Sessao(**sessao.model_dump())
    db.add(db_sessao)
    await db.commit()
    await db.refresh(db_sessao)
    return db_sessao


async def finalizar_sessao(
    db: AsyncSession,
    sessao_id: int,
    angulos_depois: dict,
    ajustes: dict
) -> Optional[Sessao]:
    """Finaliza uma sessão com os dados pós-ajuste"""
    db_sessao = await get_sessao(db, sessao_id)
    if not db_sessao:
        return None

    db_sessao.angulos_depois = angulos_depois
    db_sessao.ajustes = ajustes
    db_sessao.status = "finalizada"
    db_sessao.finalizado_em = datetime.utcnow()

    await db.commit()
    await db.refresh(db_sessao)
    return db_sessao
