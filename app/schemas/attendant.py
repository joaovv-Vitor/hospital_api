from pydantic import BaseModel, ConfigDict
from app.schemas.user import UserCreate

class AttendantBase(BaseModel):
    employee_id: str
    phone: str | None = None

# Schema unificado: recebe os dados do atendente + dados de login
class AttendantComplexCreate(AttendantBase):
    user_info: UserCreate

class AttendantResponse(AttendantBase):
    id: int
    user_id: int
    
    model_config = ConfigDict(from_attributes=True)