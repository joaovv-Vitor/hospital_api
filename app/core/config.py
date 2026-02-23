from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL: str
    
    # Configuração para ler do arquivo .env
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

settings = Settings()