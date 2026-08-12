from app.application.interfaces.audit_repository import AuditRepository
from app.application.dto.audit_dto import ListAuditsInput, AuditSummaryOutput


class ListAuditsUseCase:
    def __init__(self, audit_repository: AuditRepository):
        self._audit_repository = audit_repository

    def execute(self, input_data: ListAuditsInput) -> list[AuditSummaryOutput]:
        rows = self._audit_repository.list_all(
            production_line_id=input_data.production_line_id,
            audit_month=input_data.audit_month,
        )
        return [
            AuditSummaryOutput(
                id=audit.id,
                production_line_id=audit.production_line_id,
                audit_month=audit.audit_month,
                finding_count=finding_count,
            )
            for audit, finding_count in rows
        ]
