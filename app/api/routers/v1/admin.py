from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.api.deps import check_role

# Importamos os schemas e services necessários
from app.schemas.doctor import DoctorComplexCreate, DoctorResponse
from app.schemas.attendant import AttendantComplexCreate, AttendantResponse
from app.services import doctor as doctor_service
from app.services import attendant as attendant_service

router = APIRouter(dependencies=[Depends(check_role("admin"))])

@router.post("/doctors", response_model=DoctorResponse, status_code=status.HTTP_201_CREATED)
async def register_doctor(
    doctor_in: DoctorComplexCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Registra um novo Médico e cria suas credenciais de acesso.
    """
    return await doctor_service.create_doctor_complex(db, doctor_in)


@router.post("/attendants", response_model=AttendantResponse, status_code=status.HTTP_201_CREATED)
async def register_attendant(
    attendant_in: AttendantComplexCreate,
    db: AsyncSession = Depends(get_db)
):
    """
    Registra um novo Recepcionista/Atendente e cria suas credenciais de acesso.
    """
    return await attendant_service.create_attendant_complex(db, attendant_in)