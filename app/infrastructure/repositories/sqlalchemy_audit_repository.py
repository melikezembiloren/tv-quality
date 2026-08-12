from sqlalchemy import func
from sqlalchemy.orm import Session

from app.domain.entities.audit import Audit
from app.domain.entities.audit_finding import AuditFinding
from app.infrastructure.db.models.audit import AuditModel, AuditFindingModel


class SqlAlchemyAuditRepository:
    """AuditRepository Protocol'ünün gerçek (PostgreSQL) implementasyonu."""

    def __init__(self, session: Session):
        self._session = session

    def save(self, audit: Audit, findings: list[AuditFinding]) -> tuple[Audit, list[AuditFinding]]:
        audit_row = AuditModel(
            production_line_id=audit.production_line_id,
            audited_by_user_id=audit.audited_by_user_id,
            audit_month=audit.audit_month,
        )
        self._session.add(audit_row)
        self._session.flush()  # audit_row.id'yi commit etmeden önce almak için

        finding_rows = []
        for f in findings:
            row = AuditFindingModel(
                audit_id=audit_row.id,
                description=f.description,
                severity=f.severity,
            )
            self._session.add(row)
            finding_rows.append(row)

        self._session.commit()
        self._session.refresh(audit_row)
        for row in finding_rows:
            self._session.refresh(row)

        return self._audit_to_entity(audit_row), [self._finding_to_entity(r) for r in finding_rows]

    def get_by_id(self, audit_id: int) -> tuple[Audit, list[AuditFinding]] | None:
        audit_row = self._session.get(AuditModel, audit_id)
        if audit_row is None:
            return None

        finding_rows = (
            self._session.query(AuditFindingModel)
            .filter(AuditFindingModel.audit_id == audit_id)
            .all()
        )
        return self._audit_to_entity(audit_row), [self._finding_to_entity(r) for r in finding_rows]

    def list_all(
        self, production_line_id: int | None, audit_month: str | None
    ) -> list[tuple[Audit, int]]:
        query = self._session.query(
            AuditModel, func.count(AuditFindingModel.id)
        ).outerjoin(AuditFindingModel, AuditFindingModel.audit_id == AuditModel.id)

        if production_line_id is not None:
            query = query.filter(AuditModel.production_line_id == production_line_id)
        if audit_month is not None:
            query = query.filter(AuditModel.audit_month == audit_month)

        query = query.group_by(AuditModel.id).order_by(AuditModel.audit_month.desc())

        return [(self._audit_to_entity(row), count) for row, count in query.all()]

    @staticmethod
    def _audit_to_entity(row: AuditModel) -> Audit:
        return Audit(
            id=row.id,
            production_line_id=row.production_line_id,
            audited_by_user_id=row.audited_by_user_id,
            audit_month=row.audit_month,
            created_at=row.created_at,
        )

    @staticmethod
    def _finding_to_entity(row: AuditFindingModel) -> AuditFinding:
        return AuditFinding(
            id=row.id,
            audit_id=row.audit_id,
            description=row.description,
            severity=row.severity,
        )
