from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from datetime import date
from app.api.deps import get_current_user
from app.models.user import User

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

@router.get("/", response_model=List[AppointmentResponse])
async def list_appointments(
    # O FastAPI automaticamente entende que date_filter é um parâmetro de URL (Query Parameter)
    date_filter: date | None = None, 
    db: AsyncSession = Depends(get_db),
    # Pega o usuário logado atualmente (pelo Token JWT)
    current_user: User = Depends(get_current_user) 
):
    """
    Lista as consultas agendadas.
    - Administradores e Atendentes veem todas as consultas.
    - Médicos veem APENAS as suas próprias consultas.
    - Use 'date_filter' (YYYY-MM-DD) para buscar a agenda de um dia específico.
    """
    return await appointment_service.get_appointments(db, current_user, date_filter)