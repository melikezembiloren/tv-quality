from app.application.interfaces.audit_repository import AuditRepository
from app.application.dto.audit_dto import AuditOutput, FindingOutput


class AuditNotFoundError(Exception):
    pass


class GetAuditDetailUseCase:
    def __init__(self, audit_repository: AuditRepository):
        self._audit_repository = audit_repository

    def execute(self, audit_id: int) -> AuditOutput:
        result = self._audit_repository.get_by_id(audit_id)
        if result is None:
            raise AuditNotFoundError(f"Audit bulunamadı: id={audit_id}")

        audit, findings = result
        return AuditOutput(
            id=audit.id,
            production_line_id=audit.production_line_id,
            audited_by_user_id=audit.audited_by_user_id,
            audit_month=audit.audit_month,
            findings=[
                FindingOutput(id=f.id, description=f.description, severity=f.severity)
                for f in findings
            ],
        )
