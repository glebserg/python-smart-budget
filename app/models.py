from datetime import datetime, date

from sqlalchemy import Integer, String, DateTime, func, ForeignKey, Float, Date
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy_utils import ChoiceType
from database import Base


class BaseIDORM(Base):
    __abstract__ = True
    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)


class UserORM(BaseIDORM):
    __tablename__ = "users"
    __table_args__ = {
        "comment": "Пользователи",
    }

    first_name: Mapped[str] = mapped_column(String(20), nullable=False, comment="Имя")
    second_name: Mapped[str] = mapped_column(String(20), nullable=False, comment="Фамилия")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), comment="Дата добавления")
    updated_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=func.now(), onupdate=func.now(),
                                                 comment="Дата обновления")
    email: Mapped[str] = mapped_column(String(128), unique=True, nullable=False, comment="email")
    password_hash: Mapped[str] = mapped_column(String(128), nullable=False, comment="Хэш пароля")


class IncomeCategoryORM(BaseIDORM):
    __tablename__ = "income_categories"
    __table_args__ = {
        "comment": "Категории доходов",
    }
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    title: Mapped[str] = mapped_column(String(20), nullable=False, comment="Заголовок")
    description: Mapped[str] = mapped_column(String(20), nullable=True, comment="Описание")


class IncomeORM(BaseIDORM):
    __tablename__ = "incomes"
    __table_args__ = {
        "comment": "Доходы",
    }
    income_category_id: Mapped[int] = mapped_column(ForeignKey("income_categories.id", ondelete="SET NULL"),
                                                    comment="ID категории дохода")
    user_id: Mapped[UserORM] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), comment="ID пользователя")
    value: Mapped[float] = mapped_column(Float, comment="Значение", nullable=False)
    income_date: Mapped[date] = mapped_column(Date, comment="Дата дохода", nullable=False)


class OutlayCategoryORM(BaseIDORM):
    __tablename__ = "outlay_categories"
    __table_args__ = {
        "comment": "Категории расходов",
    }

    __allow_unmapped__ = True
    PRIORITY = (
        (0, "Обязательно"),
        (1, "Комфорт"),
        (2, "Вредно")
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"))
    priority: Mapped[int] = mapped_column(ChoiceType(PRIORITY), nullable=False,
                                          comment="Приоритет(0-обязательно, 1-комфорт, 2-вредно)")
    title: Mapped[str] = mapped_column(String(20), nullable=False, comment="Заголовок")
    description: Mapped[str] = mapped_column(String(20), nullable=True, comment="Описание")


class OutlayORM(BaseIDORM):
    __tablename__ = "outlays"
    __table_args__ = {
        "comment": "Расходы",
    }
    user_id: Mapped[UserORM] = mapped_column(ForeignKey("users.id", ondelete="CASCADE"), comment="ID пользователя")
    outlay_category_id: Mapped[int] = mapped_column(ForeignKey("outlay_categories.id", ondelete="SET NULL"),
                                                    comment="ID категории расхода")
    value: Mapped[float] = mapped_column(Float, comment="Значение", nullable=False)
    comment: Mapped[str] = mapped_column(String(100), nullable=True, comment="Комментарий")
    outlay_date: Mapped[date] = mapped_column(Date, comment="Дата расхода", nullable=False)
