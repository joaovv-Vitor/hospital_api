from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy import String, ForeignKey, DateTime, Enum as SQLAlchemyEnum
from datetime import datetime
import enum

from app.db.database import Base

# Definindo os possíveis status de uma consulta
class AppointmentStatus(str, enum.Enum):
    scheduled = "scheduled"  # Agendada
    completed = "completed"  # Concluída
    canceled = "canceled"    # Cancelada

class Appointment(Base):
    __tablename__ = "appointments"

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    
    # Chaves Estrangeiras
    patient_id: Mapped[int] = mapped_column(ForeignKey("patients.id"), nullable=False)
    doctor_id: Mapped[int] = mapped_column(ForeignKey("doctors.id"), nullable=False)
    
    # Dados da Consulta
    appointment_date: Mapped[datetime] = mapped_column(DateTime, nullable=False)
    status: Mapped[AppointmentStatus] = mapped_column(SQLAlchemyEnum(AppointmentStatus), default=AppointmentStatus.scheduled)
    notes: Mapped[str] = mapped_column(String(500), nullable=True) # Queixa principal ou observações do agendamento

    # Relacionamentos (Facilita na hora de buscar os dados completos no SQLAlchemy)
    patient = relationship("Patient")
    doctor = relationship("Doctor")