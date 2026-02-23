import uuid
import enum
from datetime import datetime

from sqlalchemy import String, Enum, DateTime
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column

from app.db.session import Base


class UserRole(str, enum.Enum):
    ADMIN = "ADMIN"
    DOCTOR = "DOCTOR"
    RECEPTIONIST = "RECEPTIONIST"


class User(Base):
    __tablename__ = "users"

    id: Mapped[uuid.UUID] = mapped_column(
        UUID(as_uuid=True),
        primary_key=True,
        default=uuid.uuid4
    )

    name: Mapped[str] = mapped_column(String(100), nullable=False)

    email: Mapped[str] = mapped_column(
        String(150),
        unique=True,
        nullable=False
    )

    password_hash: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    role: Mapped[UserRole] = mapped_column(
        Enum(UserRole),
        nullable=False
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        default=datetime.utcnow
    )