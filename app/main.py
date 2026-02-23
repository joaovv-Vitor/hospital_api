from fastapi import FastAPI
from sqlalchemy import text
from app.db.session import engine

app = FastAPI(title="Hospital API")


@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.execute(text("SELECT 1"))
    print("✅ Banco conectado com sucesso")


@app.get("/health")
async def health():
    return {"status": "ok"}