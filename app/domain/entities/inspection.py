from dataclasses import dataclass, field
from datetime import datetime, timezone

from app.domain.exceptions import DomainError

VALID_RESULTS = ("PASS", "FAIL")


class InvalidInspectionResultError(DomainError):
    """result, PASS/FAIL dışında bir değerse ya da hata bilgisiyle tutarsızsa fırlatılır."""
    pass


@dataclass
class Inspection:
    id: int | None
    tv_id: int
    result: str  # "PASS" ya da "FAIL"
    defect_category_id: int | None = None   # hata türü kataloğundan seçilen tür — FAIL'de zorunlu
    defect_reason: str | None = None        # ek açıklama — her zaman opsiyonel, serbest metin
    inspected_at: datetime = field(default_factory=lambda: datetime.now(timezone.utc))

    def __post_init__(self) -> None:
        if self.result not in VALID_RESULTS:
            raise InvalidInspectionResultError(
                f"result şunlardan biri olmalı: {VALID_RESULTS}, alınan: {self.result!r}"
            )
        if self.result == "FAIL" and self.defect_category_id is None:
            raise InvalidInspectionResultError("FAIL sonucunda hata türü (defect_category_id) zorunludur")
        if self.result == "PASS" and self.defect_category_id is not None:
            raise InvalidInspectionResultError("PASS sonucunda hata türü girilemez")
