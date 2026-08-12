from typing import Protocol
from app.domain.entities.audit import Audit
from app.domain.entities.audit_finding import AuditFinding


class AuditRepository(Protocol):
    def save(self, audit: Audit, findings: list[AuditFinding]) -> tuple[Audit, list[AuditFinding]]: ...

    def get_by_id(self, audit_id: int) -> tuple[Audit, list[AuditFinding]] | None: ...

    def list_all(
        self, production_line_id: int | None, audit_month: str | None
    ) -> list[tuple[Audit, int]]:
        """Her audit için (Audit, bulgu_sayisi) döner — liste görünümü için ağır bulgu detayını taşımaz."""
        ...
