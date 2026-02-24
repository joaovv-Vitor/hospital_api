from pydantic import BaseModel, ConfigDict
from app.schemas.user import UserCreate

class DoctorBase(BaseModel):
    crm: str
    specialty: str
    phone: str | None = None
    office_number: str | None = None
    is_active_clinical: bool = True
    user_id: int

class DoctorCreate(DoctorBase):
    pass

class DoctorResponse(DoctorBase):
    id: int
    
    model_config = ConfigDict(from_attributes=True)

class DoctorComplexCreate(BaseModel):
    # Dados do Médico
    crm: str
    specialty: str
    phone: str | None = None
    office_number: str | None = None
    
    # Dados do Usuário (reutilizando o schema que já temos)
    user_info: UserCreate