from datetime import datetime

from sqlalchemy import Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.base import Base


class ProductionRecordModel(Base):
    __tablename__ = "production_records"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tv_id: Mapped[int] = mapped_column(ForeignKey("tvs.id"), unique=True, nullable=False)
    line_id: Mapped[int] = mapped_column(ForeignKey("production_lines.id"), nullable=False)
    operator_id: Mapped[int] = mapped_column(ForeignKey("operators.id"), nullable=False)
    production_date: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    shift: Mapped[str] = mapped_column(String(20), nullable=False)
