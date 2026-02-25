from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.db.database import get_db
from app.schemas.patient import PatientCreate, PatientResponse
from app.services import patient as patient_service
from app.api.deps import get_current_user, check_role
from app.models.user import User

router = APIRouter()

