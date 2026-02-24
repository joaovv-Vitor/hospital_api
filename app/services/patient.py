from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from app.models.patient import Patient
from app.schemas.patient import PatientCreate

async def create_patient(db: AsyncSession, patient_in: PatientCreate) -> Patient:
    # Verifica se o CPF já existe
    query = select(Patient).where(Patient.cpf == patient_in.cpf)
    result = await db.execute(query)
    if result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A patient with this CPF already exists."
        )
    
    db_patient = Patient(**patient_in.model_dump())
    db.add(db_patient)
    await db.commit()
    await db.refresh(db_patient)
    return db_patient

async def get_patients(db: AsyncSession, skip: int = 0, limit: int = 100):
    query = select(Patient).offset(skip).limit(limit)
    result = await db.execute(query)
    return result.scalars().all()