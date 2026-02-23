from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker, AsyncSession
from sqlalchemy.orm import declarative_base
from app.core.config import settings

# Criando o motor de conexão assíncrono
engine = create_async_engine(
    settings.DATABASE_URL,
    echo=True, # Deixe True no desenvolvimento para ver as queries SQL no terminal
    future=True
)

# Criando a fábrica de sessões
SessionLocal = async_sessionmaker(
    bind=engine,
    class_=AsyncSession,
    expire_on_commit=False,
    autocommit=False,
    autoflush=False,
)

# Base para criarmos os nossos modelos (tabelas) depois
Base = declarative_base()

# Dependência do FastAPI para injetar o banco de dados nas rotas
async def get_db():
    async with SessionLocal() as session:
        try:
            yield session
        finally:
            await session.close()