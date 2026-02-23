import enum
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import String, Boolean, Enum
from app.db.database import Base

# 1. Definição dos perfis de acesso (Roles)
class UserRole(str, enum.Enum):
    ADMIN = "admin"
    ATTENDANT = "attendant"
    DOCTOR = "doctor"

# 2. Modelo de Utilizador para a base de dados
class User(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    email: Mapped[str] = mapped_column(String(150), unique=True, index=True, nullable=False)
    
    # Nunca guardamos a palavra-passe em texto limpo, sempre um hash (criptografia)
    hashed_password: Mapped[str] = mapped_column(String(255), nullable=False)
    
    # Atribuímos o tipo Enum à coluna para garantir que só aceita os 3 perfis definidos
    role: Mapped[UserRole] = mapped_column(Enum(UserRole), nullable=False)
    
    # Útil para o administrador desativar a conta de um médico ou atendente que saiu do hospital
    is_active: Mapped[bool] = mapped_column(Boolean, default=True)