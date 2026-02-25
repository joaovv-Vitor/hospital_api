from pydantic import BaseModel, EmailStr, ConfigDict
from app.models.user import UserRole

# 1. Adicionamos os campos na base
class UserBase(BaseModel):
    email: EmailStr
    name: str
    cpf: str
    address: str | None = None
    role: UserRole
    is_active: bool = True

class UserCreate(UserBase):
    password: str

# 2. Garantimos que a resposta devolva o nome e etc (mas nunca a senha!)
class UserResponse(UserBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)