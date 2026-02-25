from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func, cast, Date
from datetime import date

from app.models.patient import Patient
from app.models.doctor import Doctor
from app.models.appointment import Appointment, AppointmentStatus

async def get_dashboard_stats(db: AsyncSession) -> dict:
    # 1. Conta o total de pacientes
    patients_query = select(func.count(Patient.id))
    total_patients = (await db.execute(patients_query)).scalar() or 0

    # 2. Conta o total de médicos
    doctors_query = select(func.count(Doctor.id))
    total_doctors = (await db.execute(doctors_query)).scalar() or 0

    # 3. Conta quantas consultas existem APENAS na data de hoje
    today = date.today()
    appointments_today_query = select(func.count(Appointment.id)).where(
        cast(Appointment.appointment_date, Date) == today
    )
    appointments_today = (await db.execute(appointments_today_query)).scalar() or 0

    # 4. Conta quantas consultas estão com status "scheduled" (pendentes)
    pending_query = select(func.count(Appointment.id)).where(
        Appointment.status == AppointmentStatus.scheduled
    )
    pending_appointments = (await db.execute(pending_query)).scalar() or 0

    # Retorna um dicionário que bate perfeitamente com o nosso Schema
    return {
        "total_patients": total_patients,
        "total_doctors": total_doctors,
        "appointments_today": appointments_today,
        "pending_appointments": pending_appointments
    }