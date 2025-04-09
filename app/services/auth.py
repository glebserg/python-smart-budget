from authx import AuthXConfig, AuthX
from passlib.context import CryptContext
from fastapi import Request, Depends
from sqlalchemy.orm import Session

from config import auth_settings, main_settings
from database import get_db
from models import UserORM

auth_config = AuthXConfig(**auth_settings.dict())
auth_config.JWT_COOKIE_CSRF_PROTECT = not main_settings.DEBUG

security = AuthX(config=auth_config)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def get_password_hash(password: str) -> str:
    """ Функция возвращает хэш строки """
    return pwd_context.hash(password)


def verify_password(str_password: str, hash_password: str) -> bool:
    """ Функция сравнивает строковое представление пароля и хэш """
    return pwd_context.verify(str_password, hash_password)


async def get_user_by_token(request: Request, db: Session = Depends(get_db)) -> UserORM:
    from repository.user import UserRepository
    res = await security.access_token_required(request)
    return UserRepository(db).get_by_id(res.sub)
