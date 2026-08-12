import re
from dataclasses import dataclass, field
from datetime import datetime, timezone

from app.domain.exceptions import DomainError


class InvalidAuditMonthError(DomainError):
    """audit_month, 'YYYY-MM' formatında değilse fırlatılır."""
    pass


_MONTH_PATTERN = re.compile(r"^\d{4}-(0[1-9]|1[0-2])$")


@dataclass
class Audit:
    id: int | None
    production_line_id: int
    audited_by_user_id: int
    audit_month: str  # örn. "2026-08"
    created_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self) -> None:
        if not _MONTH_PATTERN.match(self.audit_month):
            raise InvalidAuditMonthError(
                f"audit_month 'YYYY-MM' formatında olmalı, alınan: {self.audit_month!r}"
            )
