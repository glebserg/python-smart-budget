from pydantic import BaseModel
from .base import DBEntityReader


class GetIncomeCategory(DBEntityReader):
    id: int
    user_id: int
    title: str
    description: str | None


class PostIncomeCategory(BaseModel):
    title: str
    description: str | None