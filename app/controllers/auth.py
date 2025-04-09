from fastapi import APIRouter, HTTPException, Response
from fastapi.params import Depends
from sqlalchemy.orm import Session

from database import get_db
from models import UserORM
from repository.user import UserRepository
from schemes.auth import PostLogin, PostRegister
from schemes.user import ResponseUser
from services.auth import security, verify_password, get_user_by_token

route = APIRouter(tags=["Авторизация"], prefix="/auth")


@route.post(
    "/register",
    description="Регистрация",
    name="Регистрация",
    response_model=ResponseUser
)
def register(creds: PostRegister, db: Session = Depends(get_db)):
    return UserRepository(db).create_user(creds)


@route.post(
    "/login",
    description="Авторизация",
    name="Авторизация"
)
def login(creds: PostLogin, response: Response, db: Session = Depends(get_db)):
    user: UserORM = UserRepository(db).get_by_email(creds.email)
    if user and verify_password(creds.password, user.password_hash):
        token = security.create_access_token(uid=str(user.id))
        security.set_access_cookies(token, response)
        return {"access_token": token}
    raise HTTPException(401, "Invalid credentials")


@route.post(
    "/logout",
    description="Выход",
    name="Выход",
    dependencies=[Depends(security.access_token_required)],
)
def logout(response: Response):
    security.unset_access_cookies(response)
    return {"detail": "Successfully logged out"}


@route.get(
    "/me",
    description="Текущий пользователь",
    name="Текущий пользователь",
    dependencies=[Depends(security.access_token_required)],
    response_model=ResponseUser
)
def me(user: UserORM = Depends(get_user_by_token)):
    return user
