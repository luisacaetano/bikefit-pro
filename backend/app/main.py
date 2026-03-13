"""
BikeFit Pro - API Principal
Sistema de análise postural para ciclistas
"""
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager

from app.config import get_settings
from app.db.database import engine, Base
from app.api.routes import pacientes, sessoes, auth, analise
from app.api.websocket import video_stream

settings = get_settings()


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Gerencia o ciclo de vida da aplicação"""
    # Startup
    print(f"🚴 Iniciando {settings.app_name} v{settings.app_version}")

    # Criar tabelas do banco de dados
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Banco de dados conectado")

    # Carregar modelo YOLOv8
    # (será carregado sob demanda para economizar memória)
    print("✅ Pronto para receber requisições")

    yield

    # Shutdown
    print("👋 Encerrando aplicação...")


# Criar aplicação FastAPI
app = FastAPI(
    title=settings.app_name,
    description="Sistema de análise postural automatizada para ciclistas usando YOLOv8-Pose",
    version=settings.app_version,
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
)

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Registrar rotas
app.include_router(auth.router, prefix="/api/auth", tags=["Autenticação"])
app.include_router(pacientes.router, prefix="/api/pacientes", tags=["Pacientes"])
app.include_router(sessoes.router, prefix="/api/sessoes", tags=["Sessões"])
app.include_router(analise.router, prefix="/api/analise", tags=["Análise"])

# Registrar WebSocket
app.include_router(video_stream.router, tags=["WebSocket"])


@app.get("/", tags=["Health"])
async def root():
    """Health check endpoint"""
    return {
        "app": settings.app_name,
        "version": settings.app_version,
        "status": "online",
        "docs": "/docs"
    }


@app.get("/health", tags=["Health"])
async def health_check():
    """Health check detalhado"""
    return {
        "status": "healthy",
        "database": "connected",
        "pose_model": settings.yolo_model
    }
