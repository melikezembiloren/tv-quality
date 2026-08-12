from app.domain.entities.audit import Audit
from app.domain.entities.audit_finding import AuditFinding
from app.application.interfaces.audit_repository import AuditRepository
from app.application.dto.audit_dto import CreateAuditInput, AuditOutput, FindingOutput


class CreateAuditUseCase:
    def __init__(self, audit_repository: AuditRepository):
        self._audit_repository = audit_repository

    def execute(self, input_data: CreateAuditInput) -> AuditOutput:
        audit = Audit(
            id=None,
            production_line_id=input_data.production_line_id,
            audited_by_user_id=input_data.audited_by_user_id,
            audit_month=input_data.audit_month,
        )

        findings = [
            AuditFinding(
                id=None,
                audit_id=None,
                description=f.description,
                severity=f.severity,
            )
            for f in input_data.findings
        ]

        saved_audit, saved_findings = self._audit_repository.save(audit, findings)

        return AuditOutput(
            id=saved_audit.id,
            production_line_id=saved_audit.production_line_id,
            audited_by_user_id=saved_audit.audited_by_user_id,
            audit_month=saved_audit.audit_month,
            findings=[
                FindingOutput(id=f.id, description=f.description, severity=f.severity)
                for f in saved_findings
            ],
        )
