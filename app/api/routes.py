from fastapi import APIRouter

# Importamos as rotas individuais
from app.api.routers.v1 import user, auth, patient, doctor, attendant

# Criamos o roteador mestre da versão 1
api_router = APIRouter()

# Registamos cada rota no roteador mestre
api_router.include_router(user.router, prefix="/users", tags=["Users"])
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])
api_router.include_router(patient.router, prefix="/patients", tags=["Patients"])
api_router.include_router(doctor.router, prefix="/doctors", tags=["Doctors"])
api_router.include_router(attendant.router, prefix="/attendants", tags=["Attendants"])
