from abc import ABC, abstractmethod

from sqlalchemy.orm import Session


class BaseRepository(ABC):
    def __init__(self, db: Session):
        self._db = db

    @abstractmethod
    async def get_by_id(self, pk: int):
        pass
