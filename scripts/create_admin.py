import asyncio
from sqlalchemy import select

from app.db.session import AsyncSessionLocal
from app.models.user import User, UserRole
from app.core.security import hash_password


async def create_admin():
    async with AsyncSessionLocal() as session:
        result = await session.execute(
            select(User).where(User.email == "admin@hospital.com")
        )
        existing = result.scalar_one_or_none()

        if existing:
            print("Admin already exists")
            return

        admin = User(
            name="Admin",
            email="admin@hospital.com",
            password_hash=hash_password("admin123"),
            role=UserRole.ADMIN,
        )

        session.add(admin)
        await session.commit()
        print("Admin created successfully")


asyncio.run(create_admin())