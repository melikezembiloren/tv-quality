from sqlalchemy import String, Integer
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.base import Base


class ProductionLineModel(Base):
    __tablename__ = "production_lines"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    code: Mapped[str] = mapped_column(String(20), unique=True, nullable=False)
    name: Mapped[str] = mapped_column(String(100), nullable=False)
    daily_target: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    weekly_target: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
    monthly_target: Mapped[int] = mapped_column(Integer, nullable=False, default=0)
