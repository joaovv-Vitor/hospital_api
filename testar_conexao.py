import asyncio
import asyncpg

async def testar_conexao():
    # A URL deve bater com as configurações do seu docker-compose.yml
    db_url = 'postgresql://postgres:banco123@localhost:5432/hospital_db'
    
    print("⏳ Tentando conectar ao banco de dados...")
    try:
        # Tenta estabelecer a conexão
        conn = await asyncpg.connect(db_url)
        print("✅ SUCESSO! Conexão com o PostgreSQL estabelecida.")
        
        # Executa uma query simples para confirmar
        versao = await conn.fetchval('SELECT version();')
        print(f"📌 Versão do Banco: {versao}")
        
        # Fecha a conexão
        await conn.close()
        
    except Exception as e:
        print(f"❌ ERRO: Não foi possível conectar ao banco de dados.\nDetalhes: {e}")

if __name__ == '__main__':
    asyncio.run(testar_conexao())