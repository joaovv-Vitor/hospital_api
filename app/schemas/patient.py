from pydantic import BaseModel, ConfigDict
from datetime import date

# Campos comuns para criação e leitura
class PatientBase(BaseModel):
    name: str
    cpf: str
    birth_date: date
    phone: str | None = None
    address: str | None = None

# Schema usado para receber dados do Swagger/Frontend (Entrada)
class PatientCreate(PatientBase):
    pass

# Schema usado para devolver dados ao cliente (Saída)
class PatientResponse(PatientBase):
    id: int

    # Permite que o Pydantic leia os dados do modelo do SQLAlchemy
    model_config = ConfigDict(from_attributes=True)