from pydantic import BaseModel, EmailStr, Field, ConfigDict
from typing import Optional

# Importamos o Enum que criámos no modelo para garantir consistência
from app.models.user import UserRole 

# 1. Esquema Base: Propriedades partilhadas
class UserBase(BaseModel):
    email: EmailStr = Field(..., description="O endereço de e-mail do utilizador")
    role: UserRole = Field(..., description="O perfil de acesso (admin, attendant, doctor)")
    is_active: Optional[bool] = Field(True, description="Indica se a conta está ativa")

# 2. Esquema para Criação: Usado quando o Administrador regista uma nova conta
class UserCreate(UserBase):
    # A palavra-passe é obrigatória na criação, com um tamanho mínimo por segurança
    password: str = Field(..., min_length=8, description="Palavra-passe com pelo menos 8 caracteres")

# 3. Esquema de Resposta: O que a API devolve (NUNCA incluímos a palavra-passe aqui)
class UserResponse(UserBase):
    id: int

    # Permite que o Pydantic leia o objeto SQLAlchemy (o nosso model User)
    model_config = ConfigDict(from_attributes=True)