from fastapi import APIRouter

# Importamos as rotas individuais
from app.api.routers.v1 import user

# Criamos o roteador mestre da versão 1
api_router = APIRouter()

# Registamos cada rota no roteador mestre
# Note que definimos o prefixo e as tags diretamente aqui, centralizando a configuração
api_router.include_router(user.router, prefix="/users", tags=["Users"])

