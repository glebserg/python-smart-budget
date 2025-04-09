from fastapi import APIRouter
from fastapi.params import Depends
from sqlalchemy.orm import Session
from sqlalchemy.util import await_only
from starlette import status

from database import get_db
from models import UserORM
from repository.income import IncomeRepository
from repository.user import UserRepository
from repository.income_categories import IncomeCategoryRepository
from schemes.income import GetIncome, PostIncome
from schemes.user import ResponseUser, RequestEditUser, ResponseUserIncomes, RequestUserIncomes
from schemes.income_category import GetIncomeCategory, PostIncomeCategory
from services.auth import security
from dependencies.owner import ResourceOwnerChecker
from dependencies.entity_exist import EntityByPK

route = APIRouter(tags=["Пользователи"])


@route.get(
    "/users",
    name="Список пользователей",
    description="Список пользователей",
    response_model=list[ResponseUser],
    dependencies=[Depends(security.access_token_required)],
)
def get_list_users(db: Session = Depends(get_db)):
    return UserRepository(db).get_all()


@route.get(
    "/users/{pk}",
    name="Детали пользователя",
    description="Детали пользователя",
    response_model=ResponseUser,
    dependencies=[
        Depends(EntityByPK(UserRepository)),
        Depends(ResourceOwnerChecker(UserRepository)),
    ],
)
def get_by_id(user: UserORM = Depends(EntityByPK(UserRepository))):
    return user


@route.put(
    "/users/{pk}",
    name="Редактировать пользователя",
    description="Редактировать пользователя",
    response_model=ResponseUser,
    dependencies=[
        Depends(EntityByPK(UserRepository)),
        Depends(ResourceOwnerChecker(UserRepository)),
    ],
)
def edit_by_id(pk: int, data: RequestEditUser, db: Session = Depends(get_db)) -> UserORM:
    return UserRepository(db).edit_by_id(pk, data)


@route.delete(
    "/users/{pk}",
    name="Удалить пользователя",
    description="Удалить пользователя",
    dependencies=[
        Depends(EntityByPK(UserRepository)),
        Depends(ResourceOwnerChecker(UserRepository)),
    ],
    status_code=status.HTTP_204_NO_CONTENT,
)
def delete_by_id(pk: int, db: Session = Depends(get_db)):
    return UserRepository(db).delete_by_id(pk)


@route.get(
    "/users/{pk}/income_categories",
    name="Категории доходов пользователя",
    description="Категории доходов пользователя",
    dependencies=[
        Depends(EntityByPK(UserRepository)),
        Depends(ResourceOwnerChecker(UserRepository)),
    ],
    response_model=list[GetIncomeCategory]
)
def get_income_categories(pk: int, db: Session = Depends(get_db)):
    return IncomeCategoryRepository(db).get_by_user_id(pk)


@route.post(
    "/users/{pk}/income_categories",
    name="Добавить категорию доходов пользователю",
    description="Добавить категорию доходов пользователю",
    dependencies=[
        Depends(EntityByPK(UserRepository)),
        Depends(ResourceOwnerChecker(UserRepository)),
    ],
    response_model=GetIncomeCategory,
)
def create_income_category_to_user(pk: int, data: PostIncomeCategory, db: Session = Depends(get_db)):
    return IncomeCategoryRepository(db).create(pk, data)


@route.get(
    "/users/{pk}/incomes",
    name="Доходы пользователя",
    description="Доходы пользователя",
    dependencies=[
        Depends(EntityByPK(UserRepository)),
        Depends(ResourceOwnerChecker(UserRepository)),
    ],
    response_model=ResponseUserIncomes,
)
def get_incomes(pk: int, db: Session = Depends(get_db), params: RequestUserIncomes = Depends()):
    return ResponseUserIncomes(incomes=IncomeRepository(db).get_by_conditions(pk, **params.model_dump()))


@route.post(
    "/users/{pk}/incomes",
    name="Добавить доход пользователю",
    description="Добавить доход пользователю",
    dependencies=[
        Depends(EntityByPK(UserRepository)),
        Depends(ResourceOwnerChecker(UserRepository)),
    ],
    response_model=GetIncome,
)
def create_income_to_user(pk: int, data: PostIncome, db: Session = Depends(get_db)):
    return IncomeRepository(db).create(pk, data)
