from typing import Type, Optional

from schemes.income_category import PostIncomeCategory
from .base import BaseRepository
from models import IncomeCategoryORM


class IncomeCategoryRepository(BaseRepository):

    def get_all(self) -> list[Type[IncomeCategoryORM]]:
        return list(self._db.query(IncomeCategoryORM).all())

    def get_by_id(self, pk: int) -> Optional[IncomeCategoryORM]:
        return self._db.query(IncomeCategoryORM).get(pk)

    def get_by_user_id(self, user_id: int) -> Optional[IncomeCategoryORM]:
        return self._db.query(IncomeCategoryORM).filter_by(user_id=user_id).all()

    def create(self, user_id: int, data: PostIncomeCategory) -> IncomeCategoryORM:
        entity = IncomeCategoryORM(**data.model_dump(), user_id=user_id)
        self._db.add(entity)
        self._db.commit()
        return entity
