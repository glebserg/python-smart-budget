import enum

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    PORT: int = 8000
    DEBUG: bool = False
    LOCAL: bool = True

    DB_USER: str = ""
    DB_PASSWORD: str = ""
    DB_HOST: str = ""
    DB_PORT: int = 5432
    DB_DB: str = ""

    @property
    def DB_URL(self) -> str:
        return "sqlite:///./sql_app.db" if self.LOCAL else f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"

    class Config:
        env_file = "../.env"


settings = Settings()
