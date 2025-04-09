from pathlib import Path
from pydantic_settings import BaseSettings


class ENVFileReader(BaseSettings):
    class Config:
        env_file = Path(__file__).parent.parent.resolve() / ".env"
        extra = "ignore"


class MainSettings(ENVFileReader):
    PORT: int = 8000
    DEBUG: bool = False
    LOCAL: bool = True


class DatabaseSettings(ENVFileReader):
    DB_USER: str = ""
    DB_PASSWORD: str = ""
    DB_HOST: str = ""
    DB_PORT: int = 5432
    DB_DB: str = ""

    @property
    def DB_URL(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_DB}"


class AuthSettings(ENVFileReader):
    JWT_SECRET_KEY: str
    JWT_TOKEN_LOCATION: list[str] = ["cookies"]
    JWT_ALGORITHM: str = "HS256"
    JWT_ACCESS_CSRF_HEADER_NAME: str = "X-CSRF-TOKEN"
    JWT_ACCESS_COOKIE_NAME: str = "smartbudget-jwt-token"
    JWT_ACCESS_CSRF_COOKIE_NAME: str = "smartbudget-csrf-token"


main_settings = MainSettings()
database_settings = DatabaseSettings()
auth_settings = AuthSettings()
