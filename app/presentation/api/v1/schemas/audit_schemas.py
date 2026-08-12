from pydantic import BaseModel


class FindingCreateRequest(BaseModel):
    description: str
    severity: str  # LOW / MEDIUM / HIGH / CRITICAL


class AuditCreateRequest(BaseModel):
    production_line_id: int
    audited_by_user_id: int
    audit_month: str  # "2026-08"
    findings: list[FindingCreateRequest] = []


class FindingResponse(BaseModel):
    id: int
    description: str
    severity: str


class AuditResponse(BaseModel):
    id: int
    production_line_id: int
    audited_by_user_id: int
    audit_month: str
    findings: list[FindingResponse] = []


class AuditSummaryResponse(BaseModel):
    id: int
    production_line_id: int
    audit_month: str
    finding_count: int
