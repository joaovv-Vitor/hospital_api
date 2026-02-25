from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status

from app.models.user import User
from app.schemas.user import UserCreate
from app.core.security import get_password_hash

async def create_user(db: AsyncSession, user_in: UserCreate) -> User:
    # 1. Verifica se o e-mail já está em uso
    query = select(User).where(User.email == user_in.email)
    result = await db.execute(query)
    existing_user = result.scalars().first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Este e-mail já está cadastrado no sistema."
        )

    # 2. Gera o hash da senha
    hashed_password = get_password_hash(user_in.password)

    # 3. Cria a instância do modelo para o banco de dados
    # Note que não passamos a senha em texto plano, apenas o hash!
    db_user = User(
        email=user_in.email,
        hashed_password=hashed_password,
        role=user_in.role,
        is_active=user_in.is_active,
        name=user_in.name,      
        cpf=user_in.cpf,         
        address=user_in.address  
    )

    # 4. Salva no banco de dados
    db.add(db_user)
    await db.commit()
    
    # Atualiza o objeto com os dados gerados pelo banco (como o ID)
    await db.refresh(db_user)

    return db_user