from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from contextlib import asynccontextmanager
from datetime import datetime, timezone

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
    description="""
    API RESTful moderna para gestão completa de um sistema hospitalar.
    
    ## Funcionalidades
    
    * 🔐 **Autenticação JWT** com controle de acesso baseado em roles
    * 👥 **Gestão de Usuários** (Admin, Médico, Atendente)
    * 🏥 **Gestão de Pacientes** com cadastro completo
    * 👨‍⚕️ **Gestão de Médicos** com especialidades e CRM
    * 📅 **Sistema de Agendamentos** com controle de status
    * 📊 **Dashboard** com estatísticas em tempo real
    
    ## Autenticação
    
    A maioria dos endpoints requer autenticação via JWT. Faça login em `/api/v1/auth/login` 
    para obter um token de acesso.
    
    ## Documentação Interativa
    
    * **Swagger UI**: `/docs` - Interface interativa para testar a API
    * **ReDoc**: `/redoc` - Documentação alternativa em formato ReDoc
    """,
    version="1.0.0",
    lifespan=lifespan,
    contact={
        "name": "Suporte API",
        "email": "suporte@hospital.com",
    },
    license_info={
        "name": "MIT",
    },
    terms_of_service="https://hospital.com/terms/",
)

# ⚠️ REGISTRO DAS ROTAS (Crucial para o Swagger funcionar)
app.include_router(api_router, prefix="/api/v1")

@app.get(
    "/",
    tags=["Informações"],
    summary="Página inicial",
    description="Retorna uma mensagem de boas-vindas da API."
)
async def root():
    """
    Endpoint raiz da API que retorna uma mensagem de boas-vindas.
    """
    return {
        "mensagem": "Bem-vindo à API do Sistema Hospitalar!",
        "versao": "1.0.0",
        "documentacao": "/docs",
        "health_check": "/health"
    }

@app.get(
    "/health",
    tags=["Health Check"],
    summary="Verificação de saúde da API",
    description="Verifica o status da API e a conexão com o banco de dados.",
    response_description="Status da API e conexão com o banco de dados"
)
async def check_db_connection(db: AsyncSession = Depends(get_db)):
    """
    Endpoint de health check que verifica:
    - Status da API (online/offline)
    - Conexão com o banco de dados PostgreSQL
    
    Retorna erro 500 se houver problemas na conexão com o banco.
    """
    try:
        result = await db.execute(text("SELECT 1"))
        return {
            "status": "online",
            "banco_de_dados": "conectado",
            "timestamp": datetime.now(timezone.utc).isoformat()
        }
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Erro na base de dados: {str(e)}"
        )