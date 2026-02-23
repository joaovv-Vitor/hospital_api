from pydantic import BaseModel, EmailStr
from uuid import UUID
from enum import Enum


class UserRole(str, Enum):
    ADMIN = "ADMIN"
    DOCTOR = "DOCTOR"
    RECEPTIONIST = "RECEPTIONIST"


class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str
    role: UserRole


class UserResponse(BaseModel):
    id: UUID
    name: str
    email: EmailStr
    role: UserRole

    class Config:
        from_attributes = True