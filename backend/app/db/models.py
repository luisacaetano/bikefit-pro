"""
Models SQLAlchemy - Tabelas do banco de dados
"""
from datetime import datetime
from sqlalchemy import Column, Integer, String, Float, DateTime, Text, ForeignKey, JSON
from sqlalchemy.orm import relationship

from app.db.database import Base


class Paciente(Base):
    """Tabela de pacientes"""
    __tablename__ = "pacientes"

    id = Column(Integer, primary_key=True, index=True)
    nome = Column(String(255), nullable=False)
    idade = Column(Integer)
    sexo = Column(String(1))  # M ou F
    altura_cm = Column(Float)
    peso_kg = Column(Float)
    telefone = Column(String(20))
    email = Column(String(255))

    # Ciclismo
    tipo_bike = Column(String(50))  # road, mtb, tri, gravel
    experiencia = Column(String(50))  # iniciante, intermediario, avancado
    km_semana = Column(Float)
    objetivo = Column(String(50))  # performance, conforto, reabilitacao

    # Histórico
    lesoes = Column(Text)
    dores = Column(Text)  # JSON string com áreas de dor
    observacoes = Column(Text)

    # Timestamps
    criado_em = Column(DateTime, default=datetime.utcnow)
    atualizado_em = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # Relacionamentos
    sessoes = relationship("Sessao", back_populates="paciente")
    medidas = relationship("Medida", back_populates="paciente")


class Sessao(Base):
    """Tabela de sessões de bike fit"""
    __tablename__ = "sessoes"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    data = Column(DateTime, default=datetime.utcnow)

    # Ângulos ANTES do ajuste
    angulos_antes = Column(JSON)  # {"knee_ext": 138, "knee_flex": 78, ...}

    # Ângulos DEPOIS do ajuste
    angulos_depois = Column(JSON)

    # Ajustes realizados
    ajustes = Column(JSON)  # {"selim_altura": "+2cm", "guidao": "sem alteração", ...}

    # Arquivos
    foto_antes_path = Column(String(500))
    foto_depois_path = Column(String(500))
    video_path = Column(String(500))
    relatorio_pdf_path = Column(String(500))

    # Observações
    observacoes = Column(Text)

    # Status
    status = Column(String(50), default="em_andamento")  # em_andamento, finalizada, cancelada

    # Timestamps
    criado_em = Column(DateTime, default=datetime.utcnow)
    finalizado_em = Column(DateTime)

    # Relacionamentos
    paciente = relationship("Paciente", back_populates="sessoes")


class Medida(Base):
    """Tabela de medidas antropométricas"""
    __tablename__ = "medidas"

    id = Column(Integer, primary_key=True, index=True)
    paciente_id = Column(Integer, ForeignKey("pacientes.id"), nullable=False)
    data = Column(DateTime, default=datetime.utcnow)

    # Medidas em cm
    entrepernas = Column(Float)
    femur = Column(Float)
    tibia = Column(Float)
    braco = Column(Float)
    antebraco = Column(Float)
    tronco = Column(Float)
    ombros_largura = Column(Float)

    # Flexibilidade
    flexibilidade_isquiotibiais = Column(String(50))  # boa, media, ruim
    toque_dedos_chao = Column(String(10))  # sim, nao, parcial

    # Relacionamentos
    paciente = relationship("Paciente", back_populates="medidas")
