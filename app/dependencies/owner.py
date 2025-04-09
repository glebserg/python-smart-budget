from typing import Type

from authx import TokenPayload
from fastapi import Depends, HTTPException, status
from sqlalchemy.orm import Session

from database import get_db
from models import BaseIDORM, UserORM
from services.auth import security
from repository.base import BaseRepository


class ResourceOwnerChecker:
    def __init__(self, resource_type: Type[BaseRepository]):
        self.resource_repository = resource_type

    def __call__(
            self,
            pk: int,
            db: Session = Depends(get_db),
            jwt: TokenPayload = Depends(security.access_token_required)
    ):
        entity: Type[BaseIDORM] = self.resource_repository(db).get_by_id(pk)
        is_owner = False
        if isinstance(entity, UserORM):
            is_owner = str(entity.id) == jwt.sub
        else:
            is_owner = str(entity.user_id.id) == jwt.sub
        if not is_owner: raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="forbidden")
