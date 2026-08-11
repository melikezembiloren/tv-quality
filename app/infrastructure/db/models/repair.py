from datetime import datetime, timezone

from sqlalchemy import Integer, ForeignKey, DateTime, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.base import Base


class RepairModel(Base):
    __tablename__ = "repairs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    defect_id: Mapped[int] = mapped_column(ForeignKey("defects.id"), nullable=False)
    repaired_by_operator_id: Mapped[int] = mapped_column(ForeignKey("operators.id"), nullable=False)
    repair_notes: Mapped[str] = mapped_column(Text, nullable=True)
    completed_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
