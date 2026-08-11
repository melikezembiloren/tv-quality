from datetime import datetime, timezone

from sqlalchemy import Integer, ForeignKey, DateTime, String
from sqlalchemy.orm import Mapped, mapped_column

from app.infrastructure.db.base import Base


class AuditModel(Base):
    __tablename__ = "audits"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    production_line_id: Mapped[int] = mapped_column(ForeignKey("production_lines.id"), nullable=False)
    audited_by_user_id: Mapped[int] = mapped_column(ForeignKey("users.id"), nullable=False)
    audit_month: Mapped[str] = mapped_column(String(7), nullable=False)  # "2026-08"
    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), default=lambda: datetime.now(timezone.utc)
    )


class AuditFindingModel(Base):
    __tablename__ = "audit_findings"

    id: Mapped[int] = mapped_column(Integer, primary_key=True, autoincrement=True)
    audit_id: Mapped[int] = mapped_column(ForeignKey("audits.id"), nullable=False)
    description: Mapped[str] = mapped_column(String(500), nullable=False)
    severity: Mapped[str] = mapped_column(String(20), nullable=False)
