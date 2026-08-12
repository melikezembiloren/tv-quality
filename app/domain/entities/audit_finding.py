from dataclasses import dataclass

from app.domain.exceptions import DomainError

VALID_SEVERITIES = ("LOW", "MEDIUM", "HIGH", "CRITICAL")


class InvalidSeverityError(DomainError):
    """severity, izin verilen değerlerden biri değilse fırlatılır."""
    pass


@dataclass
class AuditFinding:
    id: int | None
    audit_id: int | None  # Audit henüz kaydedilmemişse None olabilir
    description: str
    severity: str

    def __post_init__(self) -> None:
        if self.severity not in VALID_SEVERITIES:
            raise InvalidSeverityError(
                f"severity şunlardan biri olmalı: {VALID_SEVERITIES}, alınan: {self.severity!r}"
            )
