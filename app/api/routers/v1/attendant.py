from fastapi import APIRouter, Depends, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.attendant import AttendantComplexCreate, AttendantResponse
from app.services import attendant as attendant_service
from app.api.deps import check_role

router = APIRouter()

@router.post("/complex", response_model=AttendantResponse, status_code=status.HTTP_201_CREATED)
async def create_attendant_complete(
    attendant_in: AttendantComplexCreate,
    db: AsyncSession = Depends(get_db),
    # Apenas administradores podem cadastrar novos funcionários
    _ = Depends(check_role("admin"))
):
    """
    Cria simultaneamente as credenciais de acesso (User) e o perfil do Recepcionista (Attendant).
    """
    return await attendant_service.create_attendant_complex(db, attendant_in)