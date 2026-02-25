from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from fastapi import HTTPException, status
from datetime import timezone

from app.models.appointment import Appointment
from app.models.patient import Patient
from app.models.doctor import Doctor
from app.schemas.appointment import AppointmentCreate

async def create_appointment(db: AsyncSession, appointment_in: AppointmentCreate) -> Appointment:
    #limpar fuso
    if appointment_in.appointment_date.tzinfo is not None:
        appointment_in.appointment_date = appointment_in.appointment_date.replace(tzinfo=None)
   
    # 1. Verifica se o paciente existe
    patient_query = select(Patient).where(Patient.id == appointment_in.patient_id)
    patient_result = await db.execute(patient_query)
    if not patient_result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Paciente não encontrado."
        )

    # 2. Verifica se o médico existe
    doctor_query = select(Doctor).where(Doctor.id == appointment_in.doctor_id)
    doctor_result = await db.execute(doctor_query)
    if not doctor_result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Médico não encontrado."
        )

    # 3. Regra de Choque de Horário 
    # Garante que o médico não tenha outra consulta (não cancelada) no mesmo exato horário
    conflict_query = select(Appointment).where(
        Appointment.doctor_id == appointment_in.doctor_id,
        Appointment.appointment_date == appointment_in.appointment_date,
        Appointment.status != "canceled"
    )
    conflict_result = await db.execute(conflict_query)
    if conflict_result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="O médico já possui uma consulta ativa para este horário."
        )

    # 4. Salva a consulta se passar por todas as validações
    db_appointment = Appointment(**appointment_in.model_dump())
    db.add(db_appointment)
    await db.commit()
    await db.refresh(db_appointment)
    
    return db_appointment