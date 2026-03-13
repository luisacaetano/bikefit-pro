"""
Schemas Pydantic para Paciente
"""
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime


class PacienteBase(BaseModel):
    """Schema base para paciente"""
    nome: str
    idade: Optional[int] = None
    sexo: Optional[str] = None
    altura_cm: Optional[float] = None
    peso_kg: Optional[float] = None
    telefone: Optional[str] = None
    email: Optional[str] = None

    # Ciclismo
    tipo_bike: Optional[str] = None
    experiencia: Optional[str] = None
    km_semana: Optional[float] = None
    objetivo: Optional[str] = None

    # Histórico
    lesoes: Optional[str] = None
    dores: Optional[str] = None
    observacoes: Optional[str] = None


class PacienteCreate(PacienteBase):
    """Schema para criar paciente"""
    pass


class PacienteUpdate(BaseModel):
    """Schema para atualizar paciente (todos campos opcionais)"""
    nome: Optional[str] = None
    idade: Optional[int] = None
    sexo: Optional[str] = None
    altura_cm: Optional[float] = None
    peso_kg: Optional[float] = None
    telefone: Optional[str] = None
    email: Optional[str] = None
    tipo_bike: Optional[str] = None
    experiencia: Optional[str] = None
    km_semana: Optional[float] = None
    objetivo: Optional[str] = None
    lesoes: Optional[str] = None
    dores: Optional[str] = None
    observacoes: Optional[str] = None


class PacienteResponse(PacienteBase):
    """Schema de resposta para paciente"""
    id: int
    criado_em: datetime
    atualizado_em: datetime

    class Config:
        from_attributes = True
