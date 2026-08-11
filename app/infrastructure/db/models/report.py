from datetime import datetime, timezone

from sqlalchemy import Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.base import Base


class ReportModel(Base):
    __tablename__ = "reports"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    report_type: Mapped[str] = mapped_column(String(50), nullable=False)
    date_range_start: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    date_range_end: Mapped[datetime] = mapped_column(DateTime(timezone=True), nullable=False)
    generated_by_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    generated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
