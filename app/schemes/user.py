from datetime import datetime, date

from .base import DBEntityReader
from pydantic import BaseModel, Field, model_validator

from .income import GetIncome


class ResponseUser(DBEntityReader):
    id: int
    first_name: str
    second_name: str
    created_at: datetime
    updated_at: datetime


class RequestEditUser(BaseModel):
    first_name: str = Field(max_length=20)
    second_name: str = Field(max_length=20)


class RequestCreateUser(BaseModel):
    first_name: str = Field(max_length=20)
    second_name: str = Field(max_length=20)


class RequestUserIncomes(BaseModel):
    from_date: date | None = None
    to_date: date | None = None


class ResponseUserIncomes(BaseModel):
    total: float = 0
    incomes: list[GetIncome]

    @model_validator(mode='after')
    def calculate_sum(cls, values):
        values.total = sum([income.value for income in values.incomes])
        return values
