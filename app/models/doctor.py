from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, Boolean
from app.db.database import Base

class Doctor(Base):
    __tablename__ = "doctors"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    crm: Mapped[str] = mapped_column(String(20), unique=True, index=True, nullable=False)
    specialty: Mapped[str] = mapped_column(String(100), nullable=False)
    phone: Mapped[str] = mapped_column(String(20), nullable=True)
    office_number: Mapped[str] = mapped_column(String(10), nullable=True) # Sala de atendimento
    is_active_clinical: Mapped[bool] = mapped_column(Boolean, default=True) # Se está disponível para consultas
    
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), unique=True, nullable=False)
    user: Mapped["User"] = relationship("User")
    