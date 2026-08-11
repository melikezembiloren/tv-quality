from datetime import datetime, timezone

from sqlalchemy import Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.base import Base


class InspectionModel(Base):
    __tablename__ = "inspections"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tv_id: Mapped[int] = mapped_column(ForeignKey("tvs.id"), nullable=False)
    inspector_operator_id: Mapped[int] = mapped_column(ForeignKey("operators.id"), nullable=False)
    result: Mapped[str] = mapped_column(String(10), nullable=False)  # PASS / FAIL
    inspected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
