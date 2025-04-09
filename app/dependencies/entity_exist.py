from typing import Type, Optional
from fastapi import HTTPException, Depends, status
from sqlalchemy.orm import Session
from repository.base import BaseRepository
from database import get_db
from models import BaseIDORM


class EntityByPK:

    def __init__(self, resource_type: Type[BaseRepository]):
        self.resource_repository = resource_type

    def __call__(self, pk: int, db: Session = Depends(get_db)) -> Optional[Type[BaseIDORM]]:
        entity: Type[BaseIDORM] = self.resource_repository(db).get_by_id(pk)
        if entity:
            return entity
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND)
