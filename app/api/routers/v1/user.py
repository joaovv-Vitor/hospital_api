from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

# Importamos a dependência da base de dados
from app.db.database import get_db

# Importamos os schemas para entrada e saída de dados
from app.schemas.user import UserCreate, UserResponse

# Importamos o serviço que criámos no passo anterior
# (Damos um alias 'service_create_user' para não confundir com o nome da função da rota)
from app.services.user import create_user as service_create_user

router = APIRouter()

@router.post("/", response_model=UserResponse, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserCreate, db: AsyncSession = Depends(get_db)):
    """
    Cria um novo utilizador no sistema (Administrador, Médico ou Atendente).
    """
    # Passamos a bola para a camada de serviço que tem as regras de negócio
    user = await service_create_user(db=db, user_in=user_in)
    
    # Devolvemos o utilizador. O FastAPI e o Pydantic (UserResponse) 
    # garantem que a palavra-passe não vai na resposta!
    return user