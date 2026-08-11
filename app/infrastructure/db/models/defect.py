from datetime import datetime, timezone

from sqlalchemy import Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.base import Base


class DefectModel(Base):
    __tablename__ = "defects"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tv_id: Mapped[int] = mapped_column(ForeignKey("tvs.id"), nullable=False)
    defect_category_id: Mapped[int] = mapped_column(ForeignKey("defect_categories.id"), nullable=False)
    root_cause_id: Mapped[int | None] = mapped_column(ForeignKey("root_causes.id"), nullable=True)
    found_by_operator_id: Mapped[int] = mapped_column(ForeignKey("operators.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="OPEN")
    found_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
