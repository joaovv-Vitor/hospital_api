from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql+asyncpg://hospital_user:123456@localhost:5432/hospital"

    class Config:
        env_file = ".env"


settings = Settings()