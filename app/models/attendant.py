from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey
from app.db.database import Base

class Attendant(Base):
    __tablename__ = "attendants"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    employee_id: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=False) # Matrícula do funcionário
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    
    # Ligação com a tabela de usuários (login)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)
    user: Mapped["User"] = relationship("User")