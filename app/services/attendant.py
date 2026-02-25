from sqlalchemy.ext.asyncio import AsyncSession
from fastapi import HTTPException, status

from app.models.attendant import Attendant
from app.schemas.attendant import AttendantComplexCreate
from app.services.user import create_user as service_create_user

async def create_attendant_complex(db: AsyncSession, attendant_data: AttendantComplexCreate) -> Attendant:
    try:
        # 1. Cria o Usuário primeiro
        # Forçamos a role para garantir que não criem um admin por engano aqui
        attendant_data.user_info.role = "attendant" 
        new_user = await service_create_user(db, attendant_data.user_info)
        
        # 2. Cria o registro do Atendente usando o ID do novo usuário
        db_attendant = Attendant(
            employee_id=attendant_data.employee_id,
            phone=attendant_data.phone,
            user_id=new_user.id
        )
        
        db.add(db_attendant)
        await db.commit()
        await db.refresh(db_attendant)
        
        return db_attendant
    except Exception as e:
        await db.rollback()
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Erro ao criar atendente: {str(e)}"
        )