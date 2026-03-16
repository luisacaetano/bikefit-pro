"""
Rotas de Sessões de Bike Fit
"""
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.responses import FileResponse
from sqlalchemy.ext.asyncio import AsyncSession
from pydantic import BaseModel
from typing import List, Optional
import tempfile
import base64
import os
from pathlib import Path

from app.db.database import get_db
from app.db import crud
from app.schemas.sessao import SessaoCreate, SessaoResponse
from app.services.pdf_generator import PDFGenerator

router = APIRouter()
pdf_generator = PDFGenerator()

# Diretório para salvar imagens
UPLOADS_DIR = Path(__file__).parent.parent.parent.parent / "uploads" / "sessoes"
UPLOADS_DIR.mkdir(parents=True, exist_ok=True)


def save_base64_image(base64_data: str, sessao_id: int, tipo: str) -> str:
    """Salva imagem base64 em arquivo e retorna o path"""
    # Remove prefixo data:image/...;base64, se existir
    if "," in base64_data:
        base64_data = base64_data.split(",")[1]

    # Decodifica e salva
    image_data = base64.b64decode(base64_data)
    filename = f"sessao_{sessao_id}_{tipo}.jpg"
    filepath = UPLOADS_DIR / filename

    with open(filepath, "wb") as f:
        f.write(image_data)

    return str(filepath)


class FinalizarSessaoRequest(BaseModel):
    """Request body para finalizar sessão"""
    angulos_depois: dict
    ajustes: dict
    foto_depois_base64: Optional[str] = None


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
    # Primeiro cria a sessão para obter o ID
    db_sessao = await crud.create_sessao(db, sessao)

    # Se tiver imagem antes, salva
    foto_antes_path = None
    if sessao.foto_antes_base64:
        foto_antes_path = save_base64_image(sessao.foto_antes_base64, db_sessao.id, "antes")
        db_sessao.foto_antes_path = foto_antes_path
        await db.commit()
        await db.refresh(db_sessao)

    return db_sessao


@router.put("/{sessao_id}/finalizar", response_model=SessaoResponse)
async def finalizar_sessao(
    sessao_id: int,
    body: FinalizarSessaoRequest,
    db: AsyncSession = Depends(get_db)
):
    """Finaliza uma sessão com os dados pós-ajuste"""
    # Salva imagem depois se fornecida
    foto_depois_path = None
    if body.foto_depois_base64:
        foto_depois_path = save_base64_image(body.foto_depois_base64, sessao_id, "depois")

    sessao = await crud.finalizar_sessao(
        db, sessao_id, body.angulos_depois, body.ajustes, foto_depois_path
    )
    if not sessao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sessão não encontrada"
        )
    return sessao


@router.get("/{sessao_id}/pdf")
async def gerar_pdf_sessao(
    sessao_id: int,
    db: AsyncSession = Depends(get_db)
):
    """Gera e retorna o PDF de uma sessão"""
    # Buscar sessão
    sessao = await crud.get_sessao(db, sessao_id)
    if not sessao:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Sessão não encontrada"
        )

    # Buscar paciente
    paciente = await crud.get_paciente(db, sessao.paciente_id)
    if not paciente:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Paciente não encontrado"
        )

    # Preparar dados para o PDF
    dados = {
        "paciente": paciente.nome,
        "data": sessao.criado_em.strftime("%d/%m/%Y"),
        "angulos_antes": sessao.angulos_antes or {},
        "angulos_depois": sessao.angulos_depois or {},
        "ajustes": sessao.ajustes or {},
        "observacoes": sessao.observacoes,
        "foto_antes_path": sessao.foto_antes_path,
        "foto_depois_path": sessao.foto_depois_path,
    }

    # Gerar PDF em arquivo temporário
    with tempfile.NamedTemporaryFile(delete=False, suffix=".pdf") as tmp:
        output_path = tmp.name

    pdf_generator.generate(dados, output_path)

    filename = f"bikefit_sessao_{sessao_id}_{paciente.nome.replace(' ', '_')}.pdf"

    return FileResponse(
        output_path,
        media_type="application/pdf",
        filename=filename,
        headers={"Content-Disposition": f"attachment; filename={filename}"}
    )
