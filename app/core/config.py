from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import List
class AppConfig(BaseSettings):
    PORT: int
    HOST: str
    RELOAD: bool
    ORIGINS: List[str]
    DB_USER: str
    DB_PASSWORD: str
    DB_HOST: str
    DB_PORT: int
    DB_NAME: str
    JWT_SECRET: str
    JWT_ALGORITHM: str
    model_config = SettingsConfigDict(env_file=".env", env_prefix='APP_')
    @property
    def POSTGRES_URL(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

settings = AppConfig()