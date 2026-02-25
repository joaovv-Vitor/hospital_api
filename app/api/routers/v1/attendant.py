from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.models.user import User
from app.schemas.attendant import AttendantComplexCreate, AttendantResponse
from app.schemas.patient import PatientCreate, PatientResponse
from app.services import attendant as attendant_service
from app.schemas.patient import PatientCreate, PatientResponse
from app.services import patient as patient_service
from app.api.deps import get_current_user, check_role
from app.models.user import User

router = APIRouter()

@router.post("/", response_model=PatientResponse, status_code=status.HTTP_201_CREATED)
async def create_new_patient(
    patient_in: PatientCreate,
    db: AsyncSession = Depends(get_db),
    # APENAS Admins e Atendentes podem cadastrar
    _ : User = Depends(check_role("attendant")) 
):
    return await patient_service.create_patient(db, patient_in)

@router.get("/", response_model=list[PatientResponse])
async def list_patients(
    db: AsyncSession = Depends(get_db),
    # Médicos, Atendentes e Admins podem visualizar
    current_user: User = Depends(get_current_user)
):
    return await patient_service.get_patients(db)