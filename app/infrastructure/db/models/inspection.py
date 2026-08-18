from datetime import datetime, timezone

from sqlalchemy import Integer, ForeignKey, DateTime, String, Text
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.base import Base


class InspectionModel(Base):
    __tablename__ = "inspections"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    tv_id: Mapped[int] = mapped_column(ForeignKey("tvs.id"), nullable=False)
    # Kimin kontrol ettiği artık tutulmuyor (PIN akışı kaldırıldı) — kolon geriye dönük
    # uyumluluk için duruyor ama artık nullable, yeni kayıtlarda hiç doldurulmuyor.
    inspector_operator_id: Mapped[int | None] = mapped_column(ForeignKey("operators.id"), nullable=True)
    result: Mapped[str] = mapped_column(String(10), nullable=False)  # PASS / FAIL
    defect_category_id: Mapped[int | None] = mapped_column(ForeignKey("defect_categories.id"), nullable=True)
    defect_reason: Mapped[str | None] = mapped_column(Text, nullable=True)  # ek açıklama
    inspected_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
