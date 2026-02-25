from pydantic import BaseModel

class DashboardStats(BaseModel):
    total_patients: int
    total_doctors: int
    appointments_today: int
    pending_appointments: int