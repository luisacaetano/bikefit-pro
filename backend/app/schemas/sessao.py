"""
Schemas Pydantic para Sessão
"""
from pydantic import BaseModel
from typing import Optional, Dict, Any
from datetime import datetime


class SessaoBase(BaseModel):
    """Schema base para sessão"""
    paciente_id: int
    observacoes: Optional[str] = None


class SessaoCreate(SessaoBase):
    """Schema para criar sessão"""
    angulos_antes: Optional[Dict[str, Any]] = None


class SessaoUpdate(BaseModel):
    """Schema para atualizar sessão"""
    angulos_antes: Optional[Dict[str, Any]] = None
    angulos_depois: Optional[Dict[str, Any]] = None
    ajustes: Optional[Dict[str, Any]] = None
    observacoes: Optional[str] = None
    status: Optional[str] = None


class SessaoResponse(SessaoBase):
    """Schema de resposta para sessão"""
    id: int
    data: datetime
    angulos_antes: Optional[Dict[str, Any]] = None
    angulos_depois: Optional[Dict[str, Any]] = None
    ajustes: Optional[Dict[str, Any]] = None
    foto_antes_path: Optional[str] = None
    foto_depois_path: Optional[str] = None
    relatorio_pdf_path: Optional[str] = None
    status: str
    criado_em: datetime
    finalizado_em: Optional[datetime] = None

    class Config:
        from_attributes = True
