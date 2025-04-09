from typing import Type, Optional

from pydantic import EmailStr

from schemes.user import RequestEditUser
from services.auth import get_password_hash
from .base import BaseRepository
from models import UserORM
from app.schemes.auth import PostRegister


class UserRepository(BaseRepository):

    def get_all(self) -> list[Type[UserORM]]:
        return list(self._db.query(UserORM).all())

    def get_by_email(self, email: EmailStr) -> Optional[UserORM]:
        return self._db.query(UserORM).filter(UserORM.email == email).first()

    def get_by_id(self, pk: int) -> Optional[UserORM]:
        return self._db.query(UserORM).get(pk)

    def create_user(self, data: PostRegister) -> UserORM:
        entity = UserORM(**data.model_dump(exclude="password)"), password_hash=get_password_hash(data.password))
        self._db.add(entity)
        self._db.commit()
        return entity

    def edit_by_id(self, user_id: int, data: RequestEditUser) -> UserORM:
        entity = self.get_by_id(user_id)
        for field, value in data.model_dump().items():
            setattr(entity, field, value)
        self._db.commit()
        return entity

    def delete_by_id(self, user_id: int) -> None:
        self._db.query(UserORM).filter_by(id=user_id).delete()
        self._db.commit()
