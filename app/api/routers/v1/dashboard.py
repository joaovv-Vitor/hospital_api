from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession

from app.db.database import get_db
from app.schemas.dashboard import DashboardStats
from app.services import dashboard as dashboard_service
from app.api.deps import get_current_user
from app.models.user import User

router = APIRouter()

@router.get("/stats", response_model=DashboardStats, summary="Obtém estatísticas gerais do sistema")
async def get_stats(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """
    Retorna métricas consolidadas para a tela inicial (Dashboard).
    Permitido para: Admins e Atendentes.
    """
    if current_user.role not in ["admin", "attendant"]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, 
            detail="Acesso negado às estatísticas do sistema."
        )

    return await dashboard_service.get_dashboard_stats(db)