from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from app.core.config import settings

#from app.core.security import ALGORITHM

from app.db.database import get_db
from app.models.user import User, UserRole
from app.schemas.auth import TokenData

# Define onde a API deve procurar o token (no endpoint de login que criamos)
reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login"
)

async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(reusable_oauth2)
) -> User:
    try:
        # 1. Decodifica o Token
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]

        )
        # O 'sub' no JWT que configuramos é o email do usuário
        token_data = TokenData(email=payload.get("sub"), role=payload.get("role"))
    except (jwt.PyJWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    # 2. Busca o usuário no banco para garantir que ele ainda existe/está ativo
    query = select(User).where(User.email == token_data.email)
    result = await db.execute(query)
    user = result.scalars().first()

    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    if not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
        
    return user


def check_role(required_role: str):
    """
    Retorna uma dependência que verifica se o usuário tem o cargo necessário.
    Admins têm acesso total por padrão.
    """
    def role_verifier(current_user: User = Depends(get_current_user)):
        # Se for admin, libera sempre. Se não, checa se a role bate.
        if current_user.role != "admin" and current_user.role != required_role:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="You do not have enough privileges"
            )
        return current_user
    return role_verifier