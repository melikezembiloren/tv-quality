from dataclasses import dataclass, field
from datetime import datetime, timezone

from app.domain.exceptions import DomainError

VALID_RESULTS = ("PASS", "FAIL")


class InvalidInspectionResultError(DomainError):
    """result, PASS/FAIL dışında bir değerse ya da hata nedeniyle tutarsızsa fırlatılır."""
    pass


@dataclass
class Inspection:
    id: int | None
    tv_id: int
    inspector_operator_id: int
    result: str  # "PASS" ya da "FAIL"
    defect_reason: str | None = None
    inspected_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self) -> None:
        if self.result not in VALID_RESULTS:
            raise InvalidInspectionResultError(
                f"result şunlardan biri olmalı: {VALID_RESULTS}, alınan: {self.result!r}"
            )
        if self.result == "FAIL" and not self.defect_reason:
            raise InvalidInspectionResultError("FAIL sonucunda hata nedeni (defect_reason) zorunludur")
        if self.result == "PASS" and self.defect_reason:
            raise InvalidInspectionResultError("PASS sonucunda hata nedeni girilemez")
