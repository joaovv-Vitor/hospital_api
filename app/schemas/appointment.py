from pydantic import BaseModel, ConfigDict
from datetime import datetime
from app.models.appointment import AppointmentStatus

# Dados que são comuns em várias operações
class AppointmentBase(BaseModel):
    appointment_date: datetime
    notes: str | None = None

# Dados exigidos para CRIAR uma consulta
class AppointmentCreate(AppointmentBase):
    patient_id: int
    doctor_id: int

# Dados DEVOLVIDOS pela API
class AppointmentResponse(AppointmentBase):
    id: int
    patient_id: int
    doctor_id: int
    status: AppointmentStatus

    model_config = ConfigDict(from_attributes=True)