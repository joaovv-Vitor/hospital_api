from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.schemas.doctor import DoctorComplexCreate, DoctorCreate, DoctorResponse
from app.services import doctor as doctor_service
from app.api.deps import check_role

router = APIRouter()

@router.post("/", response_model=DoctorResponse, status_code=status.HTTP_201_CREATED)
async def create_new_doctor(
    doctor_in: DoctorCreate,
    db: AsyncSession = Depends(get_db),
    _ = Depends(check_role("admin"))
):
    return await doctor_service.create_doctor(db, doctor_in)

@router.post("/complex", response_model=DoctorResponse, status_code=status.HTTP_201_CREATED)
async def create_doctor_complete(
    doctor_in: DoctorComplexCreate,
    db: AsyncSession = Depends(get_db),
    _ = Depends(check_role("admin"))
):
    """
    Endpoint para Administradores: Cria o Usuário (Login) e o perfil do Médico em uma única operação.
    """
    return await doctor_service.create_doctor_complex(db, doctor_in)