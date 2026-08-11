from datetime import datetime, timezone

from sqlalchemy import String, Integer, ForeignKey, DateTime
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.base import Base


class TVModel(Base):
    __tablename__ = "tvs"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    serial_number: Mapped[str] = mapped_column(String(30), unique=True, nullable=False)
    line_id: Mapped[int] = mapped_column(ForeignKey("production_lines.id"), nullable=False)
    product_model_id: Mapped[int] = mapped_column(ForeignKey("product_models.id"), nullable=False)
    status: Mapped[str] = mapped_column(String(20), nullable=False, default="IN_PRODUCTION")
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )
