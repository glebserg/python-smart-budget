from datetime import date
from pydantic import BaseModel, Field

from .base import DBEntityReader


class GetIncome(DBEntityReader):
    id: int
    income_category_id: int | None
    value: float
    income_date: date


class PostIncome(BaseModel):
    income_category_id: int = Field(ge=1)
    value: float = Field(ge=.1)
    income_date: date
