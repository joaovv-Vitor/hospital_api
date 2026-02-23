from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from contextlib import asynccontextmanager

from app.db.database import engine, Base, get_db
import app.models 

# 1. Importar o nosso novo router central
from app.api.routes import api_router

@asynccontextmanager
async def lifespan(app: FastAPI):
    print("⏳ A conectar à base de dados e a criar tabelas...")
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Base de dados pronta!")
    yield 
    print("🛑 A encerrar a ligação com a base de dados...")
    await engine.dispose()

app = FastAPI(
    title="API Sistema Hospitalar",
    description="API para gestão de pacientes, médicos e consultas.",
    version="1.0.0",
    lifespan=lifespan
)

# ⚠️ REGISTRO DAS ROTAS (Crucial para o Swagger funcionar)
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    return {"mensagem": "Bem-vindo à API do Sistema Hospitalar!"}

@app.get("/health", tags=["Health Check"])
async def check_db_connection(db: AsyncSession = Depends(get_db)):
    try:
        result = await db.execute(text("SELECT 1"))
        return {"status": "online", "banco_de_dados": "conectado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro na base de dados: {str(e)}")