from fastapi import APIRouter
from app.api.routers.v1 import user, auth, patient, doctor, attendant, admin, appointment, dashboard

api_router = APIRouter()

# Rota administrativa
api_router.include_router(admin.router, prefix="/admin", tags=["Admin Control Panel"])

# Rotas normais
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(user.router, prefix="/users", tags=["Users"])
api_router.include_router(patient.router, prefix="/patients", tags=["Patients"])
api_router.include_router(doctor.router, prefix="/doctors", tags=["Doctors"])
api_router.include_router(attendant.router, prefix="/attendants", tags=["Attendants"])
api_router.include_router(appointment.router, prefix="/appointments", tags=["Appointments"])
api_router.include_router(dashboard.router, prefix="/dashboard", tags=["Dashboard & Analytics"])