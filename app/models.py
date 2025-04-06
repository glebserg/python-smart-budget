from datetime import datetime

from sqlalchemy import Integer, String, DateTime, func
from sqlalchemy.orm import Mapped, mapped_column

from database import Base


class BaseID(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)


class User(BaseID):
    first_name: Mapped[str] = mapped_column(String, max_length=20, nullable=False, comment="Имя")
    second_name: Mapped[str] = mapped_column(String, max_length=20, nullable=False, comment="Фамилия")
    created_at: Mapped[datetime] = mapped_column(DateTime, default=func.now, comment="Дата добавления")
    updated_at: Mapped[datetime] = mapped_column(DateTime, default=func.now, onupdate=True, comment="Дата обновления")
