from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.appointment import AppointmentCreate, AppointmentResponse
from app.services import appointment as appointment_service
from app.api.deps import check_role

router = APIRouter()

@router.post("/", response_model=AppointmentResponse, status_code=status.HTTP_201_CREATED)
async def schedule_appointment(
    appointment_in: AppointmentCreate,
    db: AsyncSession = Depends(get_db),
    # Apenas Atendentes (e Admins por padrão) podem agendar consultas
    _ = Depends(check_role("attendant"))
):
    """
    Agenda uma nova consulta vinculando um Paciente a um Médico em uma data e hora específicas.
    """
    return await appointment_service.create_appointment(db, appointment_in)