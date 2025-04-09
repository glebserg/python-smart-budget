from datetime import date
from typing import Type, Optional
from .base import BaseRepository
from sqlalchemy import select
from schemes.income import PostIncome
from models import IncomeORM


class IncomeRepository(BaseRepository):

    def get_by_id(self, pk: int) -> Optional[IncomeORM]:
        return self._db.query(IncomeORM).get(pk)

    def get_by_conditions(
            self,
            user_id: int,
            from_date: date = None,
            to_date: date = None,
    ) -> list[IncomeORM]:
        q = select(IncomeORM)
        q.where(IncomeORM.user_id == user_id)
        if from_date is not None:
            q = q.where(IncomeORM.income_date >= from_date)
        if to_date is not None:
            q = q.where(IncomeORM.income_date <= to_date)
        cursor = self._db.execute(q)
        return list(cursor.scalars())

    def create(self, user_id: int, data: PostIncome) -> IncomeORM:
        entity = IncomeORM(**data.model_dump(), user_id=user_id)
        self._db.add(entity)
        self._db.commit()
        return entity
