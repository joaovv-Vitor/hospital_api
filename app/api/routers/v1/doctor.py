from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from app.db.database import get_db
from app.schemas.doctor import DoctorComplexCreate, DoctorCreate, DoctorResponse
from app.services import doctor as doctor_service
from app.api.deps import check_role

router = APIRouter()

