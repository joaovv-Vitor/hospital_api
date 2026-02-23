from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from contextlib import asynccontextmanager

# Importando as configurações do banco que criamos
from app.db.database import engine, Base, get_db

# Gerenciador de ciclo de vida da aplicação (Lifespan)
@asynccontextmanager
async def lifespan(app: FastAPI):
    # --- O que acontece ao INICIAR a API ---
    print("⏳ Conectando ao banco de dados e criando tabelas...")
    async with engine.begin() as conn:
        # Cria todas as tabelas registradas na Base (útil para desenvolvimento)
        await conn.run_sync(Base.metadata.create_all)
    print("✅ Banco de dados pronto!")
    
    yield # Aqui a API fica rodando e recebendo requisições
    
    # --- O que acontece ao DESLIGAR a API ---
    print("🛑 Encerrando conexão com o banco de dados...")
    await engine.dispose()

# Inicializando o FastAPI com o lifespan
app = FastAPI(
    title="API Sistema Hospitalar",
    description="API para gerenciamento de pacientes, médicos e consultas.",
    version="1.0.0",
    lifespan=lifespan
)

@app.get("/")
async def root():
    return {"mensagem": "Bem-vindo à API do Sistema Hospitalar!"}

# Rota de teste para verificar se o FastAPI consegue falar com o Postgres
@app.get("/health", tags=["Health Check"])
async def check_db_connection(db: AsyncSession = Depends(get_db)):
    try:
        # Faz uma consulta simples no banco
        result = await db.execute(text("SELECT 1"))
        return {
            "status": "online", 
            "banco_de_dados": "conectado",
            "resultado_query": result.scalar()
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Erro ao conectar no banco: {str(e)}")