"""
Configuração do banco de dados PostgreSQL
"""
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

from app.config import get_settings

settings = get_settings()

# Converter URL para async
DATABASE_URL = settings.database_url.replace("postgresql://", "postgresql+asyncpg://")

# Criar engine async
engine = create_async_engine(
    DATABASE_URL,
    echo=settings.debug,
    future=True
)

# Session factory
async_session = async_sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)


# Base para os models
class Base(DeclarativeBase):
    pass


# Dependency para injetar sessão nas rotas
async def get_db():
    async with async_session() as session:
        try:
            yield session
        finally:
            await session.close()
