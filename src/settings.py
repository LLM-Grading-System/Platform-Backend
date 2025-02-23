from enum import Enum

from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class ApplicationMode(Enum):
    DEVELOPMENT = "dev"
    PRODUCTION = "prod"


class AppSettings(BaseSettings):
    POSTGRES_DB: str = Field(default="public")
    POSTGRES_USER: str = Field(default="postgres")
    POSTGRES_PASSWORD: str = Field(default="postgres")
    POSTGRES_PORT: int = Field(default=5432)
    POSTGRES_HOST: str = Field(default="localhost")
    MODE: ApplicationMode = Field(default=ApplicationMode.DEVELOPMENT)

    @property
    def is_dev(self) -> bool:
        return self.MODE == ApplicationMode.DEVELOPMENT

    @staticmethod
    def __generate_asyncpg_db_url(
        user: str,
        password: str,
        host: str,
        port: int,
        database_name: str,
    ) -> str:
        return f"postgresql+asyncpg://{user}:{password}@{host}:{port}/{database_name}"

    @property
    def db_url(self) -> str:
        """Get DSN for database."""
        return self.__generate_asyncpg_db_url(
            self.POSTGRES_USER,
            self.POSTGRES_PASSWORD,
            self.POSTGRES_HOST,
            self.POSTGRES_PORT,
            self.POSTGRES_DB,
        )

    model_config = SettingsConfigDict(env_file=".env", extra="ignore")


app_settings = AppSettings()
