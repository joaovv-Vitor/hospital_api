from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from app.models.doctor import Doctor
from app.models.user import User
from app.schemas.doctor import DoctorComplexCreate, DoctorCreate
from app.services.user import create_user as service_create_user
from app.models.doctor import Doctor

async def create_doctor(db: AsyncSession, doctor_in: DoctorCreate) -> Doctor:
    # 1. Verifica se o usuário existe e se é um médico
    query_user = select(User).where(User.id == doctor_in.user_id)
    result_user = await db.execute(query_user)
    user = result_user.scalars().first()
    
    if not user or user.role != "doctor":
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The provided user_id does not exist or is not a doctor."
        )

    # 2. Verifica se o CRM já está cadastrado
    query_crm = select(Doctor).where(Doctor.crm == doctor_in.crm)
    result_crm = await db.execute(query_crm)
    if result_crm.scalars().first():
        raise HTTPException(status_code=400, detail="CRM already registered.")

    db_doctor = Doctor(**doctor_in.model_dump())
    db.add(db_doctor)
    await db.commit()
    await db.refresh(db_doctor)
    return db_doctor

async def create_doctor_complex(db: AsyncSession, doctor_data: DoctorComplexCreate) -> Doctor:
    # 1. Criar o Usuário primeiro (reutilizando a lógica de hash e validação de email)
    # Importante: Garantir que a role seja 'doctor'
    doctor_data.user_info.role = "doctor" 
    new_user = await service_create_user(db, doctor_data.user_info)
    
    # 2. Criar o registro do Médico vinculado ao ID do novo usuário
    db_doctor = Doctor(
        crm=doctor_data.crm,
        specialty=doctor_data.specialty,
        phone=doctor_data.phone,
        office_number=doctor_data.office_number,
        user_id=new_user.id
    )
    
    db.add(db_doctor)
    try:
        await db.commit()
        await db.refresh(db_doctor)
    except Exception as e:
        await db.rollback()
        raise e
        
    return db_doctor