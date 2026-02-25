from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List
from datetime import date
from app.api.deps import get_current_user
from app.models.user import User

from app.db.database import get_db
from app.schemas.appointment import AppointmentCreate, AppointmentResponse, AppointmentStatusUpdate
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

@router.patch(
    "/{appointment_id}/status", 
    response_model=AppointmentResponse,
    summary="Atualiza o status de uma consulta médica",
    response_description="A consulta atualizada com o novo status."
)
async def update_status(
    appointment_id: int,
    status_in: AppointmentStatusUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Altera o estado do ciclo de vida de uma consulta (Appointment) no sistema.
    
    **Regras de Negócio e Transições de Status:**
    * scheduled: Consulta agendada (padrão ao criar).
    * completed: Consulta realizada com sucesso pelo médico.
    * canceled: Consulta desmarcada pelo paciente ou pela clínica.

    **Controle de Acesso (RBAC):**
    * **Médicos (Doctors)**: Geralmente utilizam este endpoint para marcar a consulta como completed após o atendimento.
    * **Atendentes (Attendants)** / Admins: Utilizam para marcar como canceled caso o paciente ligue desmarcando.
    
    Apenas usuários autenticados com as roles acima têm permissão para realizar esta operação.
    """
    if current_user.role not in ["admin", "attendant", "doctor"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Você não tem permissão para alterar o status de consultas."
        )

    return await appointment_service.update_appointment_status(db, appointment_id, status_in)